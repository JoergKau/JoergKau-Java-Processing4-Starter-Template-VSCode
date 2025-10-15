import processing.core.PApplet;

public class WindsurfSketch extends PApplet {

    // Colors
    int waterColor;
    int skyColor;
    int sailColor;
    int boardColor;

    // Windsurfer properties
    float boardX, boardY;
    float boardWidth = 120;
    float boardHeight = 30;
    float sailHeight = 150;
    float sailWidth = 40;
    float angle = 0;
    float windSpeed = 2;

    // Time tracking for frame-rate independence
    float lastTime;
    float elapsedTime = 0;

    public void settings() {
        size(800, 600, P2D);
    }

    public void setup() {
        smooth();
        pixelDensity(2);
        textSize(16); // Global font size

        // Initialize colors
        waterColor = color(30, 144, 255);
        skyColor = color(135, 206, 250);
        sailColor = color(255, 255, 255, 200);
        boardColor = color(139, 69, 19);

        boardX = width / 2;
        boardY = height * 0.6f;

        // Initialize time tracking
        lastTime = millis() / 1000.0f;
    }

    public void draw() {
        // Calculate delta time
        float currentTime = millis() / 1000.0f;
        float deltaTime = currentTime - lastTime;
        lastTime = currentTime;
        elapsedTime += deltaTime;

        // Update
        updateWindsurfer(deltaTime);

        // Draw
        drawBackground();
        drawWaves();
        drawWindsurfer();

        // Display wind speed and FPS
        fill(0);
        text("Wind Speed: " + nf(windSpeed, 1, 1) + " m/s", 20, 30);
        text("FPS: " + nf(frameRate, 1, 1), 20, 50);
    }

    void updateWindsurfer(float deltaTime) {
        // Update position based on wind (pixels per second)
        boardX += windSpeed * 30.0f * deltaTime;

        // Wrap around screen
        if (boardX > width + boardWidth / 2) {
            boardX = -boardWidth / 2;
        } else if (boardX < -boardWidth / 2) {
            boardX = width + boardWidth / 2;
        }

        // Slight rocking motion (time-based)
        angle = sin(elapsedTime * 3.0f) * 0.1f;
    }

    void drawBackground() {
        // Gradient sky
        for (int i = 0; i < height; i++) {
            float inter = map(i, 0, height, 0, 1);
            int c = lerpColor(skyColor, waterColor, inter);
            stroke(c);
            line(0, i, width, i);
        }
    }

    void drawWaves() {
        noStroke();
        fill(255, 255, 255, 100);

        // Draw multiple wave layers (time-based animation)
        for (int i = 0; i < 3; i++) {
            beginShape();
            vertex(0, height);
            for (int x = 0; x <= width; x += 20) {
                float y = height * 0.7f + sin(x * 0.02f + elapsedTime * 3.0f + i * 2) * 10;
                vertex(x, y);
            }
            vertex(width, height);
            endShape(CLOSE);
        }
    }

    void drawWindsurfer() {
        pushMatrix();
        translate(boardX, boardY);
        rotate(angle);

        // Draw board
        fill(boardColor);
        noStroke();
        ellipse(0, 0, boardWidth, boardHeight);

        // Draw sail
        pushMatrix();
        rotate(-angle * 2); // Sail leans with wind
        fill(sailColor);
        triangle(
                -sailWidth / 2, 0,
                sailWidth / 2, 0,
                0, -sailHeight);

        // Sail mast
        stroke(139, 69, 19);
        strokeWeight(3);
        line(0, 0, 0, -sailHeight);

        popMatrix();
        popMatrix();
    }

    public void keyPressed() {
        // Adjust wind speed with up/down arrows
        if (keyCode == UP) {
            windSpeed = min(windSpeed + 0.5f, 10);
        } else if (keyCode == DOWN) {
            windSpeed = max(windSpeed - 0.5f, 0);
        }
    }

    public void mouseDragged() {
        // Move windsurfer with mouse
        boardX = mouseX;
        boardY = mouseY;
    }

    public static void main(String[] args) {
        PApplet.main("WindsurfSketch");
    }
}
