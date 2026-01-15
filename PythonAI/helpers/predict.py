import io
import sys
import json

from trainingAI import TechnoAssistant

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.append(r'C:\Users\Dimylkin\MyProject\TechnoAssiatant\PythonAI\helpers')

# Получаем аргументы из Java
data_json = sys.argv[1]
data = json.loads(data_json)

# Вызываем метод
result = TechnoAssistant.using_model(
    "single",
    data,
    r"C:\Users\Dimylkin\MyProject\TechnoAssiatant\PythonAI\models\v1.0.0\model_RF_v1.0.0.joblib",
    r"C:\Users\Dimylkin\MyProject\TechnoAssiatant\PythonAI\models\v1.0.0\encoders_RF_v1.0.0.joblib"
)

# Возвращаем результат
print(str(result[0]))
