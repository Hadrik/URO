#ifndef ADDTAB_H
#define ADDTAB_H

#include "ItemData.h"
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QFormLayout>
#include <QPushButton>
#include <QFileDialog>
#include <QTextEdit>
#include <QLineEdit>
#include <QLabel>

class AddTab : public QWidget
{
    Q_OBJECT

    QVBoxLayout* _layout = new QVBoxLayout(this);
    QFormLayout* _layout_form = new QFormLayout();
    QHBoxLayout* _layout_image = new QHBoxLayout();

    QLineEdit* _title = new QLineEdit();
    QLineEdit* _id = new QLineEdit();
    QLineEdit* _price = new QLineEdit();
    QPushButton* _image_dialog = new QPushButton(QString("Vyberte obrázek"));
    QLabel* _image_path = new QLabel();
    QTextEdit* _description = new QTextEdit();
    QPushButton* _submit = new QPushButton(QString("Přidat"));

    QString _img_path = "";

public:
    explicit AddTab(QWidget *parent = nullptr);

public slots:
    void fill(ItemData data);

signals:
    void submit(ItemData data);

private slots:
    void _submit_clicked();
    void _load_img_path();
};

#endif // ADDTAB_H
