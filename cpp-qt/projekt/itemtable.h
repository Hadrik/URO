#ifndef ITEMTABLE_H
#define ITEMTABLE_H

#include "ItemData.h"
#include <QWidget>
#include <QTableView>
#include <QStandardItem>
#include <QVBoxLayout>
#include <QFormLayout>
#include <QLineEdit>
#include <QList>

class ItemTable : public QWidget
{
    Q_OBJECT

    QVBoxLayout* _layout = new QVBoxLayout(this);
    QFormLayout* _layout_filter = new QFormLayout();
    QLineEdit* _filter = new QLineEdit();
    QTableView* _view = new QTableView();
    QStandardItemModel* _model = new QStandardItemModel(0, 2, this);
    QList<ItemData>* _items = new QList<ItemData>; // chujsky zpusob

public:
    explicit ItemTable(QWidget *parent = nullptr);
    void set_items(const QList<ItemData>&);
    QList<ItemData> get_items();

public slots:
    void add_item(ItemData data);
    void remove_item(ItemData data);
    void remove_item(int id);

signals:
    void item_selected(ItemData data);

private slots:
    void _item_clicked(QModelIndex current);
    void _filter_items(QString text);

private:
    void table_insert(ItemData data);
    void table_remove(int id);
    void table_remove(QStandardItem* id_item);
    QStandardItem* find_item(int id);
};

#endif // ITEMTABLE_H
