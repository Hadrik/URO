#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QWidget(parent)
{
    QGridLayout* grid = new QGridLayout(this);

    text = new QLabel();
    text->setAlignment(Qt::AlignRight);

    bAC = new QPushButton("AC");
    bPN = new QPushButton("+/-");
    bPER = new QPushButton("%");
    bDIV = new QPushButton("/");
    b7 = new QPushButton("7");
    b8 = new QPushButton("8");
    b9 = new QPushButton("9");
    bMUL = new QPushButton("x");
    b4 = new QPushButton("4");
    b5 = new QPushButton("5");
    b6 = new QPushButton("6");
    bSUB = new QPushButton("-");
    b1 = new QPushButton("1");
    b2 = new QPushButton("2");
    b3 = new QPushButton("3");
    bADD = new QPushButton("+");
    b0 = new QPushButton("0");
    bDEC = new QPushButton(".");
    bEQ = new QPushButton("=");

    grid->addWidget(text, 0, 0, 1, 4);
    grid->addWidget(bAC, 1, 0);
    grid->addWidget(bPN, 1, 1);
    grid->addWidget(bPER, 1, 2);
    grid->addWidget(bDIV, 1, 3);
    grid->addWidget(b7, 2, 0);
    grid->addWidget(b8, 2, 1);
    grid->addWidget(b9, 2, 2);
    grid->addWidget(bMUL, 2, 3);
    grid->addWidget(b4, 3, 0);
    grid->addWidget(b5, 3, 1);
    grid->addWidget(b6, 3, 2);
    grid->addWidget(bSUB, 3, 3);
    grid->addWidget(b1, 4, 0);
    grid->addWidget(b2, 4, 1);
    grid->addWidget(b3, 4, 2);
    grid->addWidget(bADD, 4, 3);
    grid->addWidget(b0, 5, 0, 1, 2);
    grid->addWidget(bDEC, 5, 2);
    grid->addWidget(bEQ, 5, 3);

    setLayout(grid);

    QVector<QPushButton*> digits = {b0, b1, b2, b3, b4, b5, b6, b7, b8, b9};
    for (const auto button : digits){
        connect(button, SIGNAL(clicked()), this, SLOT(number_press()));
    }

    QVector<QPushButton*> operators = {bADD, bSUB, bMUL, bDIV};
    for (const auto button : operators){
        connect(button, SIGNAL(clicked()), this, SLOT(operator_press()));
    }

    connect(bAC, SIGNAL(clicked()), this, SLOT(clear()));
    connect(bEQ, SIGNAL(clicked()), this, SLOT(calc()));
    connect(bDEC, SIGNAL(clicked()), this, SLOT(decimal()));
    connect(bPN, SIGNAL(clicked()), this, SLOT(change_sign()));
    connect(bPER, SIGNAL(clicked()), this, SLOT(percent()));
}

MainWindow::~MainWindow() {}

void MainWindow::number_press() {
    auto clicked = qobject_cast<QPushButton*>(sender());
    auto digit = clicked->text();
    text->setText(text->text() + digit);
}

void MainWindow::operator_press() {
    auto clicked = qobject_cast<QPushButton*>(sender());
    storedValue = text->text().toDouble();
    pendingOp = clicked->text();
    text->clear();
}

void MainWindow::clear() {
    text->clear();
    pendingOp.clear();
}

void MainWindow::calc() {
    auto newVal = text->text().toDouble();
    if (pendingOp == "+") {
        text->setText(QString::number(storedValue + newVal));
    } else if (pendingOp == "-") {
        text->setText(QString::number(storedValue - newVal));
    } else if (pendingOp == "x") {
        text->setText(QString::number(storedValue * newVal));
    } else if (pendingOp == "/") {
        text->setText(QString::number(storedValue / newVal));
    }
}

void MainWindow::decimal() {
    if (text->text().contains('.')) return;

    text->setText(text->text() + '.');
}

void MainWindow::change_sign() {
    auto t = text->text();
    auto val = t.toDouble();
    if (val > 0.0) {
        text->setText('-' + t);
    } else if (val < 0.0) {
        text->setText(t.removeFirst());
    }
}

void MainWindow::percent() {
    text->setText(QString::number(text->text().toDouble() / 100));
}
