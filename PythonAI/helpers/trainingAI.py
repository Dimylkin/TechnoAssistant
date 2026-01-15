import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder


class TechnoAssistant:
    @staticmethod
    def training_model(path_to_dataset, path_to_model_for_save, path_to_encoders_for_save):
        df = pd.read_csv(path_to_dataset).drop(['link', 'general_score'], axis=1)

        encoders = {}
        for column_name in df.columns:
            if df[column_name].dtype == object:
                le = LabelEncoder()
                df[column_name] = le.fit_transform(df[column_name].astype(str))
                encoders[column_name] = le

        X = df.drop('estimation', axis=1)
        y = df['estimation']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        TechnoAssistant.save_model(model, path_to_model_for_save, encoders, path_to_encoders_for_save)
        TechnoAssistant.graphics(X, X_test, y_test, model,encoders)

    @staticmethod
    def open_model(path_to_model, path_to_encoders):
        return joblib.load(path_to_model), joblib.load(path_to_encoders)

    @staticmethod
    def save_model(model, path_to_model, encoders, path_to_encoders):
        joblib.dump(model, path_to_model)
        joblib.dump(encoders, path_to_encoders)

    @staticmethod
    def using_model(type_data, dataset, path_to_model, path_to_encoders):
        if type_data == "test":
            df = pd.read_csv(dataset).drop(['link', 'general_score'], axis=1)
            model, encoders = TechnoAssistant.open_model(path_to_model, path_to_encoders)

            for column_name in df.columns:
                if column_name in encoders:
                    known_classes = encoders[column_name].classes_
                    df[column_name] = df[column_name].astype(str).apply(
                        lambda x: x if x in known_classes else known_classes[0]
                    )
                    df[column_name] = encoders[column_name].transform(df[column_name])
        else:
            df = pd.DataFrame([dataset])
            model, encoders = TechnoAssistant.open_model(path_to_model, path_to_encoders)

            for column_name in df.columns:
                if column_name in encoders and column_name != 'estimation':
                    known_classes = encoders[column_name].classes_
                    df[column_name] = df[column_name].astype(str).apply(
                        lambda x: x if x in known_classes else known_classes[0]
                    )
                    df[column_name] = encoders[column_name].transform(df[column_name])

        model, encoders = TechnoAssistant.open_model(path_to_model, path_to_encoders)
        prediction = model.predict(df)
        return encoders['estimation'].inverse_transform(prediction)

    @staticmethod
    def graphics(X, X_test, y_test, model, encoders):
        y_pred = model.predict(X_test)

        # Декодируем классы обратно в исходные названия
        le_estimation = encoders['estimation']
        class_labels = le_estimation.classes_
        y_test_decoded = le_estimation.inverse_transform(y_test)
        y_pred_decoded = le_estimation.inverse_transform(y_pred)

        # Настройка стиля
        plt.style.use('seaborn-v0_8-darkgrid')
        fig = plt.figure(figsize=(16, 10))

        # 1. Матрица ошибок с исходными названиями классов
        ax1 = plt.subplot(2, 3, 1)
        cm = confusion_matrix(y_test_decoded, y_pred_decoded, labels=class_labels)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True, square=True,
                    xticklabels=class_labels, yticklabels=class_labels)
        plt.title('Матрица ошибок', fontsize=14, fontweight='bold')
        plt.ylabel('Истинные значения')
        plt.xlabel('Предсказанные значения')

        # 2. Важность признаков
        ax2 = plt.subplot(2, 3, 2)
        importances = model.feature_importances_
        feature_names = X.columns
        indices = importances.argsort()[::-1][:10]
        plt.barh(range(len(indices)), importances[indices], color='teal')
        plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
        plt.xlabel('Важность')
        plt.title('Важность признаков (Top 10)', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()

        # 3. Точность модели
        ax3 = plt.subplot(2, 3, 3)
        accuracy = accuracy_score(y_test_decoded, y_pred_decoded)
        sizes = [accuracy * 100, (1 - accuracy) * 100]
        colors = ['#66b3ff', '#ff9999']
        explode = (0.1, 0)
        plt.pie(sizes, explode=explode, labels=['Правильно', 'Ошибки'],
                colors=colors, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 12})
        plt.title(f'Точность модели: {accuracy:.2%}', fontsize=14, fontweight='bold')

        # 4. Распределение предсказаний с исходными названиями
        ax4 = plt.subplot(2, 3, 4)
        pred_counts = pd.Series(y_pred_decoded).value_counts().reindex(class_labels, fill_value=0)
        plt.bar(range(len(pred_counts)), pred_counts.values, color='coral', edgecolor='black')
        plt.xlabel('Классы')
        plt.ylabel('Количество')
        plt.title('Распределение предсказаний', fontsize=14, fontweight='bold')
        plt.xticks(range(len(class_labels)), class_labels, rotation=45, ha='right')

        # 5. Метрики классификации с исходными названиями
        ax5 = plt.subplot(2, 3, 5)
        report_dict = classification_report(y_test_decoded, y_pred_decoded,
                                            labels=class_labels, output_dict=True, zero_division=0)
        metrics_data = pd.DataFrame({
            'precision': [report_dict[cls]['precision'] for cls in class_labels],
            'recall': [report_dict[cls]['recall'] for cls in class_labels],
            'f1-score': [report_dict[cls]['f1-score'] for cls in class_labels]
        })
        x_pos = range(len(class_labels))
        width = 0.25
        plt.bar([p - width for p in x_pos], metrics_data['precision'], width, label='Precision', color='skyblue')
        plt.bar(x_pos, metrics_data['recall'], width, label='Recall', color='lightgreen')
        plt.bar([p + width for p in x_pos], metrics_data['f1-score'], width, label='F1-Score', color='salmon')
        plt.xlabel('Классы')
        plt.ylabel('Значение')
        plt.title('Метрики по классам', fontsize=14, fontweight='bold')
        plt.xticks(x_pos, class_labels, rotation=45, ha='right')
        plt.legend()
        plt.ylim(0, 1.1)

        # 6. Сравнение истинных и предсказанных значений
        ax6 = plt.subplot(2, 3, 6)
        comparison = pd.DataFrame({'Истинные': y_test_decoded, 'Предсказанные': y_pred_decoded})
        comparison_counts = comparison.groupby(['Истинные', 'Предсказанные']).size().unstack(fill_value=0)
        comparison_counts = comparison_counts.reindex(index=class_labels, columns=class_labels, fill_value=0)
        comparison_counts.plot(kind='bar', stacked=False, ax=ax6, colormap='Set2')
        plt.xlabel('Истинные классы')
        plt.ylabel('Количество')
        plt.title('Сравнение истинных и предсказанных', fontsize=14, fontweight='bold')
        plt.legend(title='Предсказанные', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45, ha='right')

        plt.tight_layout()
        plt.show()

        print("=" * 60)
        print(f"{'РЕЗУЛЬТАТЫ ОБУЧЕНИЯ':^60}")
        print("=" * 60)
        print(f"Исходные классы: {', '.join(class_labels)}")
        print(f"Точность модели: {accuracy:.2%}")
        print(f"Правильных предсказаний: {sum(y_test_decoded == y_pred_decoded)} из {len(y_test_decoded)}")
        print("\n" + "-" * 60)
        print("Детальный отчёт по классам:")
        print("-" * 60)
        print(classification_report(y_test_decoded, y_pred_decoded, labels=class_labels, zero_division=0))

