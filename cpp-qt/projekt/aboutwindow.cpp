#include "aboutwindow.h"

AboutWindow::AboutWindow(QWidget *parent)
    : QWidget{parent}
{
    _window->setWindowTitle("Informace");

    QLabel* text1 = new QLabel("Program na evidenci produktů v obchodě");
    text1->setAlignment(Qt::AlignCenter);
    _layout->addWidget(text1);
    QLabel* text2 = new QLabel("TRA0117");
    text2->setAlignment(Qt::AlignCenter);
    _layout->addWidget(text2);

    _window->setLayout(_layout);
}

void AboutWindow::show() {
    _window->exec();
}
