#include "addtab.h"

AddTab::AddTab(QWidget *parent)
    : QWidget{parent}
{
    _layout_form->addRow("Název", _title);
    _layout_form->addRow("ID", _id);
    _layout_form->addRow("Cena", _price);
    _layout->addLayout(_layout_form);

    _layout_image->addWidget(_image_dialog);
    _layout_image->addWidget(_image_path);
    _layout->addLayout(_layout_image);

    _layout->addWidget(new QLabel("Info"));
    _layout->addWidget(_description);

    _layout->addWidget(_submit);

    setLayout(_layout);

    connect(_submit, SIGNAL(pressed()), this, SLOT(_submit_clicked()));
    connect(_image_dialog, SIGNAL(pressed()), this, SLOT(_load_img_path()));
}

void AddTab::fill(ItemData data) {
    _title->setText(data.title);
    _id->setText(QString::number(data.id));
    _price->setText(QString::number(data.price));
    _description->setText(data.description);
    _image_path->setText(data.img_path);
}

void AddTab::_submit_clicked() {
    ItemData data {
            _id->text().toInt(),
            _title->text(),
            _price->text().toDouble(),
            _description->toPlainText(),
            _img_path
    };
    emit submit(data);


}

void AddTab::_load_img_path() {
    _img_path = QFileDialog::getOpenFileName(this, "Načíst obrázek");
    _image_path->setText(_img_path);
}
