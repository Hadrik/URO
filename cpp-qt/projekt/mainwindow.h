#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "itemtable.h"
#include "tabpanel.h"
#include "aboutwindow.h"
#include "itemloader.h"
#include <QMainWindow>
#include <QHBoxLayout>
#include <QAction>
#include <QMenu>
#include <QPalette>
#include <QColorDialog>

QT_BEGIN_NAMESPACE
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

    QHBoxLayout* _layout = new QHBoxLayout(this);

    ItemTable* _itemtable = new ItemTable();
    TabPanel* _tabpanel = new TabPanel();

    QAction* _show_about;
    QMenu* _settings_menu;
    QAction* _load_items;
    QAction* _save_items;
    QAction* _change_color;

    AboutWindow* _window_about = new AboutWindow();

    ItemLoader _loader;

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void _save();
    void _load();
    void _new_color();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
