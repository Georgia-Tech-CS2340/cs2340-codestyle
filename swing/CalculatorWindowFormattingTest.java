import java.awt.Dimension;
import java.util.function.BiFunction;

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

/**
 * Main window component that displays calculator UI
 * ;;;;
 * ** Intentionally poorly formatted to test checkstyle ** ;
 */
public class CalculatorWindowFormattingTest {
    private static final String[] OPERANDS = {"A", "B"};
    private static final  String HEADER_TEXT = "Java Swing Calculator Demo";
    private static final int FORM_PADDING = 0;
    private static final int OUTER_PADDING = 6;
    private static final int SPACING = 6;
    private static final int[] DEFAULT_SIZE = {400, 500};
    private static final int FORM_LINE_HEIGHT = 36;
    private static final int OPERATION_LEFT_SPACING = 16;
    private static final int COMBO_BOX_WIDTH = 150;
    private static final String RESULT_FORMAT = "Result: %s";
    private static final String[] OPERATIONS = {"+", "-", "*", "/", "^", "%"};
    @SuppressWarnings("unchecked")
    private static final BiFunction<Integer, Integer, Integer>[] OPERATION_FUNCTIONS =
        (BiFunction<Integer, Integer, Integer>[]) new BiFunction[] {
            (a, b) -> ((int) a + (int) b) ,
            (a, b) -> ((int) a - (int) b),
            (a, b) -> ((int) a * (int) b),
            (a, b) -> ((int) a / (int) b),
            (a, b) -> ((int) Math.pow((int) a, (int) b)),
            (a, b) -> ((int) a % (int) b) };

    private JFrame root;
    private JLabel resultLabel;
    private String[] operands = new String[OPERANDS.length];
    private int currentOperation;

    public CalculatorWindowFormattingTest(){
        this.root = new JFrame();
        this.root.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        this.root.setContentPane(this.CONSTRUCT_LAYOUT());
        this.root.setSize(DEFAULT_SIZE[0], DEFAULT_SIZE[1]);
    }

    public void show() {
        this.root.setVisible(true);
    }

    protected JPanel CONSTRUCT_LAYOUT () {
        JPanel rootLayout = new JPanel();
        rootLayout.setLayout(new BoxLayout(rootLayout,BoxLayout.PAGE_AXIS));
        rootLayout.setBorder(BorderFactory.createEmptyBorder(OUTER_PADDING,OUTER_PADDING,OUTER_PADDING,OUTER_PADDING));

        JLabel label = new JLabel(HEADER_TEXT);
        JPanel labelLayout = new JPanel();
        labelLayout.setLayout(new BoxLayout(labelLayout, BoxLayout.LINE_AXIS));
        labelLayout.add(label);
        rootLayout.add(labelLayout);

        rootLayout.add(Box.createRigidArea(new Dimension(0, SPACING)));
        rootLayout.add(this.createForm());

        rootLayout.add(Box.createRigidArea(new Dimension(0, SPACING)));
        rootLayout.add(this.createResults());

        return rootLayout;
    }

    protected JPanel createForm() {
        JPanel panel = new JPanel(new SpringLayout());
        for (int i = 0; i < OPERANDS.length; ++i) {
            JLabel lbl = new JLabel(OPERANDS[i], JLabel.TRAILING);
            lbl.setBorder(new EmptyBorder(0, 0, SPACING, SPACING));

            JTextField txtField = new JTextField("");
            txtField.setMaximumSize(new Dimension(Integer.MAX_VALUE, FORM_LINE_HEIGHT));
            final int textIndex = i;
            txtField.getDocument().addDocumentListener(new DocumentListener() {
                @Override public void insertUpdate(DocumentEvent e) {
                    update();
                }
                @Override public void removeUpdate(DocumentEvent e) {
                 update();
                }
                @Override public void changedUpdate(DocumentEvent e) {
                    update();
                }
                private void update() {
                    operands[textIndex] = txtField.getText();
                    invalidate();
                }
            });

            lbl.setLabelFor(txtField);
            panel.add(lbl);
            panel.add(txtField);
            this.operands[i] = txtField.getText();
        }

        SpringUtilities.makeCompactGrid(panel, OPERANDS.length, 2,
                FORM_PADDING, FORM_PADDING, FORM_PADDING, FORM_PADDING);
        return panel;
    }

    protected JPanel createResults() {
        JPanel panel = new JPanel();
        panel.setMaximumSize(new Dimension(Integer.MAX_VALUE, FORM_LINE_HEIGHT));
        panel.setLayout(new BoxLayout(panel, BoxLayout.LINE_AXIS));

        JComboBox<String> operationSelector = new JComboBox<>(OPERATIONS);
        operationSelector.setSelectedIndex(0);
        operationSelector.setMaximumSize(new Dimension(COMBO_BOX_WIDTH, Integer.MAX_VALUE));
        operationSelector.addActionListener(e -> {
            @SuppressWarnings("unchecked")
            JComboBox<String> cb = (JComboBox<String>) e.getSource();
            setCurrentOperation(cb.getSelectedIndex());
        });
        this.currentOperation = 0;
        panel.add(Box.createRigidArea(new Dimension(OPERATION_LEFT_SPACING, 0)));
        panel.add(operationSelector);

        JLabel resultLabel = new JLabel(String.format(RESULT_FORMAT, ""));
        this.resultLabel = resultLabel;
        panel.add(Box.createRigidArea(new Dimension(SPACING, 0)));
        panel.add(resultLabel);

        panel.add(Box.createHorizontalGlue());

        return panel; }

    protected void resetResult() {
        this.resultLabel.setText(String.format(RESULT_FORMAT, ""));
    }

    protected void setResult(int newResult) {
        this.resultLabel.setText(String.format(RESULT_FORMAT, String.valueOf(newResult)));
    }

    protected void setCurrentOperation(int newOperation) {
        int old = this.currentOperation;
        this.currentOperation = newOperation;
        if (old != newOperation) {
            this.invalidate();
        }
    }

    protected void invalidate() {
        boolean canPerformOperation = isInteger(operands[0]) && isInteger(operands[1]);
        if (canPerformOperation) {
            int a = Integer.parseInt(operands[0]);
            int b = Integer.parseInt(operands[1]);
            int result = OPERATION_FUNCTIONS[this.currentOperation].apply(a, b);
            this.setResult(result);
        } else {
            this.resetResult();
        }
    }

    protected boolean isInteger(String val) {
        try {
            Integer.parseInt(val);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }
}
