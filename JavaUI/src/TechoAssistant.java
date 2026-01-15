package src;

import java.io.BufferedReader;
import java.io.InputStreamReader;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.GridPane;
import javafx.stage.Stage;

public class TechoAssistant extends Application {

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("Techno Assistant");

        GridPane grid = new GridPane();
        grid.setHgap(10);
        grid.setVgap(10);
        grid.setPadding(new Insets(10, 10, 10, 10));

        // Все поля для модели
        TextField priceField = new TextField();
        TextField osField = new TextField();
        TextField newField = new TextField();
        TextField modelCpuField = new TextField();
        TextField coreField = new TextField();
        TextField frequencyField = new TextField();
        TextField socketField = new TextField();
        TextField ramGbField = new TextField();
        TextField ramTypeField = new TextField();
        TextField ramGhzField = new TextField();
        TextField modelGpuField = new TextField();
        TextField vramGbField = new TextField();
        TextField storageGbField = new TextField();
        TextField motherBoardField = new TextField();
        TextField powerSupplyField = new TextField();

        // Добавляем все поля
        grid.add(new Label("price:"), 0, 0);
        grid.add(priceField, 1, 0);
        
        grid.add(new Label("os:"), 0, 1);
        grid.add(osField, 1, 1);
        
        grid.add(new Label("new:"), 0, 2);
        grid.add(newField, 1, 2);
        
        grid.add(new Label("model_cpu:"), 0, 3);
        grid.add(modelCpuField, 1, 3);
        
        grid.add(new Label("core:"), 0, 4);
        grid.add(coreField, 1, 4);
        
        grid.add(new Label("frequency_ghz:"), 0, 5);
        grid.add(frequencyField, 1, 5);
        
        grid.add(new Label("socket:"), 0, 6);
        grid.add(socketField, 1, 6);
        
        grid.add(new Label("ram_gb:"), 0, 7);
        grid.add(ramGbField, 1, 7);
        
        grid.add(new Label("ram_type:"), 0, 8);
        grid.add(ramTypeField, 1, 8);
        
        grid.add(new Label("ram_ghz:"), 0, 9);
        grid.add(ramGhzField, 1, 9);
        
        grid.add(new Label("model_gpu:"), 0, 10);
        grid.add(modelGpuField, 1, 10);
        
        grid.add(new Label("vram_gb:"), 0, 11);
        grid.add(vramGbField, 1, 11);
        
        grid.add(new Label("storage_gb:"), 0, 12);
        grid.add(storageGbField, 1, 12);
        
        grid.add(new Label("mother_board:"), 0, 13);
        grid.add(motherBoardField, 1, 13);
        
        grid.add(new Label("power_supply:"), 0, 14);
        grid.add(powerSupplyField, 1, 14);

        Button submitButton = new Button("Отправить");
        grid.add(submitButton, 0, 15, 2, 1);

        Label resultLabel = new Label("");
        grid.add(resultLabel, 0, 16, 2, 1);

        submitButton.setOnAction(event -> {
        	
        	String jsonData = String.format(
        	        "{\\\"price\\\":\\\"%s\\\",\\\"os\\\":\\\"%s\\\",\\\"new\\\":\\\"%s\\\",\\\"model_cpu\\\":\\\"%s\\\"," +
        	        "\\\"core\\\":\\\"%s\\\",\\\"frequency_ghz\\\":\\\"%s\\\",\\\"socket\\\":\\\"%s\\\",\\\"ram_gb\\\":\\\"%s\\\"," +
        	        "\\\"ram_type\\\":\\\"%s\\\",\\\"ram_ghz\\\":\\\"%s\\\",\\\"model_gpu\\\":\\\"%s\\\",\\\"vram_gb\\\":\\\"%s\\\"," +
        	        "\\\"storage_gb\\\":\\\"%s\\\",\\\"mother_board\\\":\\\"%s\\\",\\\"power_supply\\\":\\\"%s\\\"}",
        	        priceField.getText(), osField.getText(), newField.getText(),
        	        modelCpuField.getText(), coreField.getText(), frequencyField.getText(),
        	        socketField.getText(), ramGbField.getText(), ramTypeField.getText(),
        	        ramGhzField.getText(), modelGpuField.getText(), vramGbField.getText(),
        	        storageGbField.getText(), motherBoardField.getText(), powerSupplyField.getText()
        	    );
        	
//        	String jsonData = "{\\\"price\\\":\\\"85000\\\",\\\"os\\\":\\\"windows 11 home\\\",\\\"new\\\":\\\"yes\\\"," +
//                    "\\\"model_cpu\\\":\\\"intel core i5-12400f\\\",\\\"core\\\":\\\"6\\\"," +
//                    "\\\"frequency_ghz\\\":\\\"4.4\\\",\\\"socket\\\":\\\"lga1700\\\"," +
//                    "\\\"ram_gb\\\":\\\"16\\\",\\\"ram_type\\\":\\\"ddr4\\\",\\\"ram_ghz\\\":\\\"3200\\\"," +
//                    "\\\"model_gpu\\\":\\\"nvidia geforce rtx 3060\\\",\\\"vram_gb\\\":\\\"12\\\"," +
//                    "\\\"storage_gb\\\":\\\"512\\\",\\\"mother_board\\\":\\\"asus prime b660m-a\\\"," +
//                    "\\\"power_supply\\\":\\\"650\\\"}";



            try {
                ProcessBuilder pb = new ProcessBuilder(
                    "python",
                    "C:\\Users\\Dimylkin\\MyProject\\TechnoAssiatant\\PythonAI\\helpers\\predict.py",
                    jsonData
                );
                pb.redirectErrorStream(true);
                Process process = pb.start();

                // Читаем ВСЕ строки вывода
                BufferedReader reader = new BufferedReader(
                    new InputStreamReader(process.getInputStream(), "UTF-8")
                );
                
                StringBuilder output = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line).append("\n");
                }
                
                process.waitFor();
                
                // Выводим полный результат (включая ошибки)
                System.out.println("Python output:");
                System.out.println(output.toString());
                
                resultLabel.setText("Результат: " + output.toString());

            } catch (Exception e) {
                resultLabel.setText("Ошибка Java: " + e.getMessage());
                e.printStackTrace();
            }
        });

        Scene scene = new Scene(grid, 500, 600);
        primaryStage.setScene(scene);
        primaryStage.show();
    }
}
