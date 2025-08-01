import javax.swing.*;
import java.awt.*;

public class TriforceFractale extends JPanel {

    private final int profondeurMax = 6; // profondeur de récursion (augmente pour plus de détails)

    public void drawTriforce(Graphics2D g, int x, int y, int size, int depth) {
        if (depth == 0) return;

        int height = (int) (Math.sqrt(3) / 2 * size);

        // Triangle haut
        drawTriangle(g, x + size / 2, y, size / 2);

        // Triangle bas gauche
        drawTriangle(g, x, y + height / 2, size / 2);

        // Triangle bas droite
        drawTriangle(g, x + size / 2, y + height / 2, size / 2);

        // Appels récursifs
        drawTriforce(g, x + size / 4, y, size / 2, depth - 1);
        drawTriforce(g, x, y + height / 2, size / 2, depth - 1);
        drawTriforce(g, x + size / 2, y + height / 2, size / 2, depth - 1);
    }

    public void drawTriangle(Graphics2D g, int x, int y, int size) {
        int height = (int) (Math.sqrt(3) / 2 * size);
        Polygon triangle = new Polygon();
        triangle.addPoint(x, y);
        triangle.addPoint(x - size / 2, y + height);
        triangle.addPoint(x + size / 2, y + height);
        g.setColor(Color.YELLOW);
        g.fillPolygon(triangle);
        g.setColor(Color.BLACK);
        g.drawPolygon(triangle);
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        drawTriforce((Graphics2D) g, getWidth() / 4, 50, getWidth() / 2, profondeurMax);
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Triforce Fractale");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 700);
        frame.add(new TriforceFractale());
        frame.setVisible(true);
    }
}
