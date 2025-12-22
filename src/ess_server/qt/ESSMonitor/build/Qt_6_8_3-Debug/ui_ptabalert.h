/********************************************************************************
** Form generated from reading UI file 'ptabalert.ui'
**
** Created by: Qt User Interface Compiler version 6.8.3
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_PTABALERT_H
#define UI_PTABALERT_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_pTabAlert
{
public:

    void setupUi(QWidget *pTabAlert)
    {
        if (pTabAlert->objectName().isEmpty())
            pTabAlert->setObjectName("pTabAlert");
        pTabAlert->resize(400, 300);

        retranslateUi(pTabAlert);

        QMetaObject::connectSlotsByName(pTabAlert);
    } // setupUi

    void retranslateUi(QWidget *pTabAlert)
    {
        pTabAlert->setWindowTitle(QCoreApplication::translate("pTabAlert", "Form", nullptr));
    } // retranslateUi

};

namespace Ui {
    class pTabAlert: public Ui_pTabAlert {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_PTABALERT_H
