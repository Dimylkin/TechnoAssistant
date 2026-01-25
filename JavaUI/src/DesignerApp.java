package src;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.effect.ColorAdjust;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

/**
 * Main application class for the Designer application.
 * Provides a JavaFX-based UI with a title bar, scrollable content area, and customizable form card.
 * Extends JavaFX Application class to create and manage the primary window.
 */
public class DesignerApp extends Application {
	
	/**
	 * Root container for the entire application layout.
	 */
	public VBox root;
	
	/**
	 * Container for the main content area within the scroll pane.
	 */
	public VBox contentBox;
	
	/**
	 * Card container for form elements with rounded corners and shadow effect.
	 */
	public VBox formCard;
	
	/**
	 * Scroll pane that wraps the content area to enable vertical scrolling.
	 */
	public ScrollPane scrollPane;
	
	/**
	 * Primary stage (main window) of the application.
	 */
	public Stage primaryStage;
	
	/**
	 * Color adjustment effect used to dim the application interface.
	 */
	public ColorAdjust dimEffect = new ColorAdjust();
    
	/**
	 * Title text displayed in the application's title bar and window title.
	 */
	public String title;
	
	/**
	 * Constructs a DesignerApp instance with specified stage and title.
	 * Automatically initializes and displays the application window.
	 *
	 * @param primary The primary stage for this application
	 * @param title The title to display in the title bar and window
	 */
	public DesignerApp(Stage primary, String title) {
		this.primaryStage = primary;
		this.title = title;
		
		start(primary);
	}
	
	/**
	 * Main entry point for the JavaFX application.
	 * Launches the application when run as a standalone program.
	 *
	 * @param args Command line arguments
	 */
	public static void main(String[] args) {
        launch(args);
    }
	
	/**
	 * Initializes and displays the primary stage with all UI components.
	 * Sets up the root layout, title bar, content area, and scene.
	 *
	 * @param primary The primary stage to configure and display
	 */
	@Override
    public void start(Stage primary) {
        root = new VBox();
        root.setStyle("-fx-background-color: #f5f5f5;");
        
        HBox titleHBox = createTitleBar();
        
        ScrollPane scrollPane = createContentArea();
        VBox.setVgrow(scrollPane, Priority.ALWAYS);
        
        root.getChildren().addAll(titleHBox, scrollPane);
        
        Scene scene = new Scene(root, 1280, 1024); 
        
        primaryStage.setTitle(title);
        primaryStage.setScene(scene);
        primaryStage.show();
    }
	
	/**
	 * Creates and configures the title bar component.
	 * Returns an HBox with centered title label and purple gradient background.
	 *
	 * @return Configured HBox containing the title label
	 */
	public HBox createTitleBar() {
        HBox titleHBox = new HBox();
        titleHBox.setAlignment(Pos.CENTER);
        titleHBox.setPadding(new Insets(20));
        titleHBox.setStyle("-fx-background-color: #667eea;");
        
        Label titleLabel = new Label(title);
        titleLabel.setStyle("-fx-text-fill: white; -fx-font-size: 24px; -fx-font-weight: bold;");
        titleHBox.getChildren().add(titleLabel);
        
        return titleHBox;
    }
	
	/**
	 * Creates and configures the scrollable content area.
	 * Initializes the content box and form card within a scroll pane.
	 *
	 * @return Configured ScrollPane containing the content area
	 */
	private ScrollPane createContentArea() {
        scrollPane = new ScrollPane();
        scrollPane.setFitToWidth(true);
        scrollPane.setStyle("-fx-background-color: transparent; -fx-background: #f5f5f5;");
        
        contentBox = new VBox(20);
        contentBox.setPadding(new Insets(30));
        contentBox.setAlignment(Pos.TOP_CENTER);
        
        formCard = createFormCard();
        contentBox.getChildren().add(formCard);
        
        scrollPane.setContent(contentBox);
        return scrollPane;
    }
	
	/**
	 * Creates a styled card container for form elements.
	 * Returns a VBox with white background, rounded corners, and drop shadow.
	 *
	 * @return Configured VBox styled as a form card
	 */
	private VBox createFormCard() {
        VBox card = new VBox(20);
        card.setMaxWidth(800);
        card.setPadding(new Insets(30));
        card.setAlignment(Pos.CENTER);
        card.setStyle(
            "-fx-background-color: white;" +
            "-fx-background-radius: 15;" +
            "-fx-effect: dropshadow(gaussian, rgba(0,0,0,0.1), 20, 0, 0, 5);"
        );
        
        return card;
    }
	
	/**
	 * Applies or removes a dimming effect on the entire application interface.
	 * Uses ColorAdjust effect to reduce brightness when dimmed.
	 *
	 * @param dim True to apply dimming effect, false to remove it
	 */
	public void dimApplication(boolean dim) {
        if (dim) {
            dimEffect.setBrightness(-0.5);
        } else {
            dimEffect.setBrightness(0.0);
        }
        root.setEffect(dimEffect);
    }
	
	/**
	 * Returns CSS style string for button elements based on hover state.
	 * Provides different background colors for normal and hovered states.
	 *
	 * @param isEntered True if mouse is hovering over the button, false otherwise
	 * @return CSS style string for the button
	 */
	public String getStyleButton(boolean isEntered) {
		if (isEntered == true) {
			return "-fx-background-color: #5568d3;" +
	                "-fx-text-fill: white;" +
	                "-fx-font-size: 16px;" +
	                "-fx-font-weight: bold;" +
	                "-fx-padding: 15 30;" +
	                "-fx-background-radius: 25;" +
	                "-fx-cursor: hand;";
		}
		else {
			return "-fx-background-color: #667eea;" +
	                "-fx-text-fill: white;" +
	                "-fx-font-size: 16px;" +
	                "-fx-font-weight: bold;" +
	                "-fx-padding: 15 30;" +
	                "-fx-background-radius: 25;" +
	                "-fx-cursor: hand;";
		}
	}
}
