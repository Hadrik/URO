#include "itemloader.h"

ItemLoader::ItemLoader(QObject *parent)
    : QObject{parent}
{}

void ItemLoader::save(QList<ItemData> data) {
    QString path = QFileDialog::getSaveFileName(nullptr, "Exportovat");

    // ukladani
}

QList<ItemData> ItemLoader::load() {
    QString path = QFileDialog::getOpenFileName(nullptr, "Importovat");

    // nacitani

    return QList<ItemData> {
        {1, "Item 1", 10, "Item 1 description", "images/mechanical_keyboard.png"},
        {2, "Item 2", 20, "Item 2 description", ""},
        {3, "Item 3", 30, "Item 3 description", ""}
    };
}
