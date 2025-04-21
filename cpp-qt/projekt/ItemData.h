#ifndef ITEMDATA_H
#define ITEMDATA_H

#include <QString>

typedef struct ItemData {
    int id;
    QString title;
    double price;
    QString description;
    QString img_path;
} ItemData;

#endif // ITEMDATA_H
