#ifndef ABOUTWINDOW_H
#define ABOUTWINDOW_H

#include <QWidget>
#include <QDialog>
#include <QLabel>
#include <QVBoxLayout>

class AboutWindow : public QWidget
{
    Q_OBJECT

    QDialog* _window = new QDialog();
    QVBoxLayout* _layout = new QVBoxLayout();

public:
    explicit AboutWindow(QWidget *parent = nullptr);

public slots:
    void show();
};

#endif // ABOUTWINDOW_H
