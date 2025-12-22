/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.8.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QVBoxLayout *verticalLayout;
    QTabWidget *pTabWidget;
    QWidget *pTabMain;
    QWidget *pTabEnv;
    QWidget *pTabAlert;
    QWidget *pTabAccess;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(800, 600);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        verticalLayout = new QVBoxLayout(centralwidget);
        verticalLayout->setObjectName("verticalLayout");
        pTabWidget = new QTabWidget(centralwidget);
        pTabWidget->setObjectName("pTabWidget");
        pTabMain = new QWidget();
        pTabMain->setObjectName("pTabMain");
        pTabWidget->addTab(pTabMain, QString());
        pTabEnv = new QWidget();
        pTabEnv->setObjectName("pTabEnv");
        pTabWidget->addTab(pTabEnv, QString());
        pTabAlert = new QWidget();
        pTabAlert->setObjectName("pTabAlert");
        pTabWidget->addTab(pTabAlert, QString());
        pTabAccess = new QWidget();
        pTabAccess->setObjectName("pTabAccess");
        pTabWidget->addTab(pTabAccess, QString());

        verticalLayout->addWidget(pTabWidget);

        MainWindow->setCentralWidget(centralwidget);

        retranslateUi(MainWindow);

        pTabWidget->setCurrentIndex(3);


        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        pTabWidget->setTabText(pTabWidget->indexOf(pTabMain), QCoreApplication::translate("MainWindow", "Main", nullptr));
        pTabWidget->setTabText(pTabWidget->indexOf(pTabEnv), QCoreApplication::translate("MainWindow", "Environment", nullptr));
        pTabWidget->setTabText(pTabWidget->indexOf(pTabAlert), QCoreApplication::translate("MainWindow", "Alert", nullptr));
        pTabWidget->setTabText(pTabWidget->indexOf(pTabAccess), QCoreApplication::translate("MainWindow", "Access Log", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
