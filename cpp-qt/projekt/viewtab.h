#ifndef VIEWTAB_H
#define VIEWTAB_H

#include "ItemData.h"
#include <QWidget>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QPushButton>
#include <QLabel>
#include <QTextEdit>
#include <QGraphicsScene>
#include <QGraphicsView>

class ViewTab : public QWidget
{
    Q_OBJECT

    QVBoxLayout* _layout = new QVBoxLayout(this);

    QLabel* _title = new QLabel();
    QLabel* _id = new QLabel();
    QLabel* _price = new QLabel();
    QLabel* _description_label = new QLabel(QString("Dodatečné informace"));
    QTextEdit* _description = new QTextEdit();

    QGraphicsScene* _img_scene = new QGraphicsScene();
    QGraphicsView* _img_view = new QGraphicsView(_img_scene);

    QHBoxLayout* _button_layout = new QHBoxLayout();
    QPushButton* _button_remove = new QPushButton(QString("Odstranit"));
    QPushButton* _button_edit = new QPushButton(QString("Upravit"));

    ItemData _current;

public:
    explicit ViewTab(QWidget *parent = nullptr);

public slots:
    void display(ItemData data);

signals:
    void remove_item(int id);
    void edit_item(ItemData data);

private slots:
    void remove_click();
    void edit_click();
};

#endif // VIEWTAB_H
