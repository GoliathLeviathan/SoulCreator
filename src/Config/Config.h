/**
 * \file
 * \author Victor von Rhein <victor@caern.de>
 *
 * \section License
 *
 * Copyright (C) 2011 by Victor von Rhein
 *
 * This file is part of SoulCreator.
 *
 * SoulCreator is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * SoulCreator is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with SoulCreator.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef CONFIG_H
#define CONFIG_H

#include <QString>
#include <QColor>
#include <QFont>

/**
 * @brief Konfigurationsklasse des Programms.
 *
 * Hier werden die Konfigurationseinstellungen gespeichert.
 */

class Config {
	public:
		/**
		 * Der Name des Programms.
		 */
		static QString name();
		/**
		 * Major-Versionsnummer.
		 *
		 * Die gesamte Versionsnummer besteht aus Major.Minor.Change.
		 */
		static const int versionMajor;
		/**
		 * Minor-Versionsnummer.
		 *
		 * Die gesamte Versionsnummer besteht aus Major.Minor.Change.
		 */
		static const int versionMinor;
		/**
		 * Change-Versionsnummer.
		 *
		 * Die gesamte Versionsnummer besteht aus Major.Minor.Change.
		 */
		static const int versionChange;
		/**
		 * Die aktuelle Version des Programms ausschließlich der Change-Nummer.
		 *
		 * Programme mit unterschieldicher Versionsnummer sind zueinander nicht notwendigerweise kompatibel.
		 */
		static QString version();
		/**
		 * Die aktuelle Version des Programms einschließlich der Change-Nummer.
		 *
		 * Unterscheiden sich Programme in ihrer Change-Nummer, aber der Rest ihrer Versionsnummer ist gleich, sollten eigentlich keine Kompatibilitätsprobleme mit den Template-Dateien und den gespeicherten Charakteren auftreten.
		 */
		static QString versionDetail();
		/**
		 * Der Name der organisation, welche hinter diesem Programm steht.
		 */
		static const QString organization;
		/**
		 * Name der Konfigurationsdatei für dieses Programm.
		 */
		static const QString configFile;
		/**
		 * Normaler vertikaler Abstand. Wird für Widgets eingesetzt, die zwar untereinander erscheinen, abe rnicht zusammengequetscht erscheinen sollen.
		 */
		static const int vSpace;
		/**
		 * Der Pixelabstand zwischen Eigenschaftsblöcken. Beispielsweise der vertikale Abstand zwischen Den Fertigkeiten der verschiedenen Kategorien.
		 */
		static const int traitCategorySpace;
		/**
		 * Die Anzahl, wie oft Eigenschaften mit Beschreibungstext mehrfach ausgewählt werden dürfen.
		 */
		static const int traitMultipleMax;
		/**
		 * DieMinimale Breite für Textfelder für zusätzlichen Text von Eigenschaften.
		 */
		static const int traitCustomTextWidthMin;
		/**
		 * Die größtmögliche Höhe von Widgets, welche sich in einer Textzeile befinden.
		 *
		 * Diese Höhe wurde gewählt, um vertikalen Raum zu sparen.
		 */
		static const int inlineWidgetHeightMax;
		/**
		 * Die Breite der Armor-Spinboxes.
		 */
		static const int spinBoxNoTextWidth;
		/**
		 * Die Breite einer einfachen Vertikalen Eigenschaftsliste.
		 **/
		static const int traitListVertivalWidth;
		/**
		 * Die Zeit, wie lange Nachrichten in der Statuszeile angezeigt werden sollen.
		 */
		static const int displayTimeout;
		/**
		 * Wichtige Textabschnitte sollen in dieser Farbe erscheinen. Diese Funktion gibt den Farbnamen aus.
		 *
		 * \note Für die Farbe siehe auch importantTextColor().
		 **/
		static QString importantTextColorName();
		/**
		 * Wichtige Textabschnitte sollen in dieser Farbe erscheinen.
		 *
		 * \note Für den Farbnamen siehe auch importantTextColorName().
		 **/
		static QColor importantTextColor();
		/**
		 * Warnfarbe, wenn zuviele Punkte vergeben wurden.
		 **/
		static const QColor pointsNegative;
		/**
		 * Warnfarbe, wenn zuwenige Punkte vergeben wurden.
		 **/
		static const QColor pointsPositive;
		/**
		 * Das Standardverzeichnis, in welchem die zu speichernden Charaktere abgelegt werden sollen.
		 **/
		static QString saveDir();
		/**
		 * Eigenschaftshöchstwert.
		 **/
		static const int traitMax;
		/**
		 * Höchstwert der Moral.
		 **/
		static const int moralityTraitMax;
		/**
		 * Höchstwert der Moral bei der ein Charakter eine Geistesstörung haben kann.
		 **/
		static const int derangementMoralityTraitMax;
		/**
		 * Startwert der Moral.
		 **/
		static const int moralityTraitDefaultValue;
		/**
		 * Höchstwert der Willenskraft.
		 **/
		static const int willpowerMax;
		/**
		 * Mindestwert der besonderen übernatürlichen Eigenschaft.
		 **/
		static const int superTraitMin;
		/**
		 * Höchstwert der besonderen übernatürlichen Eigenschaft.
		 **/
		static const int superTraitMax;
		/**
		 * Startwert der besonderen übernatürlichen Eigenschaft.
		 **/
		static const int superTraitDefaultValue;

		/**
		 * Über wievielen Punkten die Eigenschaften 2 Erschaffungspunkte kosten.
		 *
		 * Alle Punkte bis einschließelich dieser Zahl kosten nur 1 Punkt pro Punkt, aber alle darüber kosten das Doppelte.
		 **/
		static const int creationTraitDouble;

		/**
		 * Schriftgröße für den normalen Text auf dem ausdruckbaren Charakterbogen.
		 **/
		static const qreal textSizeFactorPrintNormal;
		/**
		 * Schriftgröße für den kleinen Text auf dem ausdruckbaren Charakterbogen.
		 **/
		static const qreal textSizeFactorPrintSmall;

		/**
		 * Die Schriftart, welche für den exportierten Charakter verwendet wird.
		 **/
		static QFont exportFont;
		/**
		 * Die Schriftart, welche für das Programm verwendet wird.
		 **/
		static QFont windowFont;

	private:
		Config();
};

#endif


