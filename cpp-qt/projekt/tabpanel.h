#ifndef TABPANEL_H
#define TABPANEL_H

#include "ItemData.h"
#include "addtab.h"
#include "viewtab.h"
#include <QWidget>
#include <QVBoxLayout>
#include <QTabWidget>
#include <QFrame>

class TabPanel : public QWidget
{
    Q_OBJECT

    QVBoxLayout* _layout = new QVBoxLayout(this);
    QTabWidget* _panel = new QTabWidget();
    AddTab* _tab_add = new AddTab();
    ViewTab* _tab_view = new ViewTab();

public:
    explicit TabPanel(QWidget *parent = nullptr);

public slots:
    void display_item(ItemData data);
    void display_item_edit(ItemData data);

signals:
    void add_item(ItemData);
    void remove_item(int);
};

#endif // TABPANEL_H
