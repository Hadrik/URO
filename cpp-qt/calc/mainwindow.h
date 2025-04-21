#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include <QGridLayout>
#include <QLabel>

class MainWindow : public QWidget
{
    Q_OBJECT

    QLabel* text;

    QPushButton* bAC;
    QPushButton* bPN;
    QPushButton* bPER;
    QPushButton* bDIV;
    QPushButton* b7;
    QPushButton* b8;
    QPushButton* b9;
    QPushButton* bMUL;
    QPushButton* b4;
    QPushButton* b5;
    QPushButton* b6;
    QPushButton* bSUB;
    QPushButton* b1;
    QPushButton* b2;
    QPushButton* b3;
    QPushButton* bADD;
    QPushButton* b0;
    QPushButton* bDEC;
    QPushButton* bEQ;

    double storedValue;
    QString pendingOp;

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

public slots:
    void number_press();
    void operator_press();
    void clear();
    void calc();
    void decimal();
    void change_sign();
    void percent();
};
#endif // MAINWINDOW_H
