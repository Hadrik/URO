#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    setWindowTitle("Úžasná aplikace");

    _show_about = new QAction("O Aplikaci");
    _settings_menu = new QMenu("Nastavení");
    _load_items = new QAction("Importovat");
    _save_items = new QAction("Exportovat");
    _change_color = new QAction("Změnit barvu");
    _settings_menu->addAction(_load_items);
    _settings_menu->addAction(_save_items);
    _settings_menu->addAction(_change_color);
    menuBar()->addMenu(_settings_menu);
    menuBar()->addAction(_show_about);

    _layout->addWidget(_itemtable);
    _layout->addWidget(_tabpanel);

    centralWidget()->setLayout(_layout);

    connect(_itemtable, SIGNAL(item_selected(ItemData)), _tabpanel, SLOT(display_item(ItemData)));
    connect(_tabpanel, SIGNAL(remove_item(int)), _itemtable, SLOT(remove_item(int)));
    connect(_tabpanel, SIGNAL(add_item(ItemData)), _itemtable, SLOT(add_item(ItemData)));
    connect(_show_about, SIGNAL(triggered()), _window_about, SLOT(show()));
    connect(_load_items, SIGNAL(triggered()), this, SLOT(_load()));
    connect(_save_items, SIGNAL(triggered()), this, SLOT(_save()));
    connect(_change_color, SIGNAL(triggered()), this, SLOT(_new_color()));
}

void MainWindow::_save() {
    _loader.save(_itemtable->get_items());
}

void MainWindow::_load() {
    _itemtable->set_items(_loader.load());
}

void MainWindow::_new_color() {
    QColor color = QColorDialog::getColor(Qt::white, this);
    QColor dark = color.darker();
    QColor light = color.lighter();
    if (!color.isValid()) return;
    QPalette palette = qApp->palette();
    palette.setColor(QPalette::Base, color);
    palette.setColor(QPalette::Window, dark);
    palette.setColor(QPalette::Button, light);
    qApp->setPalette(palette);
}

MainWindow::~MainWindow()
{
    delete ui;
}
