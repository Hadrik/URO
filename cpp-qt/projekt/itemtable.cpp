#include "itemtable.h"
#include <QHeaderView>

ItemTable::ItemTable(QWidget *parent)
    : QWidget{parent}
{
    _layout_filter->addRow("Filtr", _filter);
    _layout->addLayout(_layout_filter);

    _model->setHeaderData(0, Qt::Horizontal, QString("ID"));
    _model->setHeaderData(1, Qt::Horizontal, QString("Název"));

    _view->setModel(_model);
    _view->setSelectionBehavior(QAbstractItemView::SelectRows);
    _view->setSelectionMode(QAbstractItemView::SingleSelection);
    _view->setEditTriggers(QAbstractItemView::NoEditTriggers);

    _view->horizontalHeader()->setVisible(true);
    _view->horizontalHeader()->setStretchLastSection(true);
    _view->verticalHeader()->setVisible(false);

    _layout->addWidget(_view);
    setLayout(_layout);

    connect(_view, SIGNAL(clicked(QModelIndex)), this, SLOT(_item_clicked(QModelIndex)));
    connect(_filter, SIGNAL(textChanged(QString)), this, SLOT(_filter_items(QString)));
}

void ItemTable::add_item(ItemData data) {
    QStandardItem* existing_item_id = find_item(data.id);
    if (existing_item_id == nullptr) {
        // adding
        table_insert(data);
    } else {
        // editing
        int row = existing_item_id->row();
        _model->item(row, 1)->setText(data.title);
        for (auto& item : *_items) {
            if (item.id == data.id) {
                item = data;
                break;
            }
        }
    }
}

void ItemTable::remove_item(ItemData data) {
    remove_item(data.id);
}

void ItemTable::remove_item(int id) {
    QStandardItem* item = find_item(id);
    if (item == nullptr) {
        // item with id not found - throw?
        return;
    }

    table_remove(item);
    
    for (int i = 0; i < _items->size(); ++i) {
        if ((*_items)[i].id == id) {
            _items->removeAt(i);
            break;
        }
    }
}

void ItemTable::_item_clicked(QModelIndex current) {
    if (!current.isValid()) return;

    int id = _model->item(current.row(), 0)->text().toInt();

    for (auto& item : *_items) {
        if (item.id == id) {
            emit item_selected(item);
            break;
        }
    }
}

void ItemTable::_filter_items(QString filter) {
    for (int i = 0; i < _model->rowCount(); i++) {
        QStandardItem* title_item = _model->item(i, 1);
        QString title = title_item->text();

        if (title.contains(filter, Qt::CaseInsensitive)) {
            _view->showRow(i);
        } else {
            _view->hideRow(i);
        }
    }
}

void ItemTable::table_insert(ItemData data) {
    QStandardItem* idItem = new QStandardItem(QString::number(data.id));
    QStandardItem* titleItem = new QStandardItem(data.title);

    QList<QStandardItem*> row = {idItem, titleItem};
    _model->appendRow(row);
    _items->append(data);
}

void ItemTable::table_remove(int id) {
    QStandardItem* item = find_item(id);
    if (item == nullptr) return;
    table_remove(item);
}

void ItemTable::table_remove(QStandardItem* id_item) {
    int row = id_item->row();
    _model->removeRow(row);
}

QStandardItem* ItemTable::find_item(int id) {
    for (int i = 0; i < _model->rowCount(); ++i) {
        QStandardItem* item = _model->item(i, 0);
        auto data = item->text();
        if (data.toInt() == id) {
            return item;
        }
    }
    return nullptr;
}

void ItemTable::set_items(const QList<ItemData>& data) {
    _items->clear();
    for (const auto& item : data) {
        _items->append(item);
        table_insert(item);
    }
}

QList<ItemData> ItemTable::get_items() {
    return *_items;
}
