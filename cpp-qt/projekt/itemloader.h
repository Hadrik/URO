#ifndef ITEMLOADER_H
#define ITEMLOADER_H

#include "ItemData.h"
#include <QObject>
#include <QList>
#include <QFileDialog>

class ItemLoader : public QObject
{
    Q_OBJECT
public:
    explicit ItemLoader(QObject *parent = nullptr);

    void save(QList<ItemData>);
    QList<ItemData> load();

signals:
};

#endif // ITEMLOADER_H
