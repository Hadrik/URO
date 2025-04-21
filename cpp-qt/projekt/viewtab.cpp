#include "viewtab.h"

ViewTab::ViewTab(QWidget *parent)
    : QWidget{parent}
{
    _description->setReadOnly(true);

    _layout->addWidget(_title);
    _layout->addWidget(_id);
    _layout->addWidget(_price);
    _layout->addWidget(_description_label);
    _layout->addWidget(_description);
    _layout->addWidget(_img_view);

    _button_layout->addWidget(_button_remove);
    _button_layout->addWidget(_button_edit);

    _layout->addLayout(_button_layout);

    setLayout(_layout);

    connect(_button_remove, SIGNAL(pressed()), this, SLOT(remove_click()));
    connect(_button_edit, SIGNAL(pressed()), this, SLOT(edit_click()));
}

void ViewTab::display(ItemData data) {
    _current = data;
    _title->setText(data.title);
    _id->setText(QString("ID: ").append(QString::number(data.id)));
    _price->setText(QString::number(data.price).append(" Kč"));
    _description->setText(data.description);

    QString path = data.img_path;
    if (!path.startsWith("C:")) {
        path = path.prepend("../../");
    }
    _img_scene->clear();
    QPixmap pm;
    bool has_img = pm.load(path);
    if (has_img) {
        _img_scene->addPixmap(pm);
    } else {
        _img_scene->addPixmap(QPixmap("../../Image-not-found.png"));
    }
}

void ViewTab::remove_click() {
    int id = _id->text().toInt();
    if (id) return;
    emit remove_item(id);
}

void ViewTab::edit_click() {
    if (_id->text().toInt() < 0) return;

    emit edit_item(_current);
}
