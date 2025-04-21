#include "tabpanel.h"

TabPanel::TabPanel(QWidget *parent)
    : QWidget{parent}
{
    _panel->addTab(_tab_add, QString("Přidat"));
    _panel->addTab(_tab_view, QString("Zobrazit"));

    _layout->addWidget(_panel);
    setLayout(_layout);

    connect(_tab_view, SIGNAL(remove_item(int)), this, SIGNAL(remove_item(int)));
    connect(_tab_view, SIGNAL(edit_item(ItemData)), this, SLOT(display_item_edit(ItemData)));
    connect(_tab_add, SIGNAL(submit(ItemData)), this, SIGNAL(add_item(ItemData)));
}

void TabPanel::display_item(ItemData data) {
    _tab_view->display(data);
    _panel->setCurrentWidget(_tab_view);
}

void TabPanel::display_item_edit(ItemData data) {
    _tab_add->fill(data);
    _panel->setCurrentWidget(_tab_add);
}
