#!/usr/bin/env python

import customtkinter as ctk
import os
from PIL import Image
import mysql.connector as sql
import re
import math


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.change_appearance_mode_event("System")

        self.conn = sql.connect(
            host="mysql-omar-yossuf.alwaysdata.net",
            user="356467",
            passwd="Omar1244",
            database="omar-yossuf_tvsat",
        )

        self.cur = self.conn.cursor()

        self.user = ""
        self.login_flag = False

        self.cur.execute("SELECT DISTINCT name FROM satellite")
        self.sats = self.cur.fetchall()

        for i in range(len(self.sats)):
            self.sats[i] = self.sats[i][0]

        self.cur.execute("SELECT DISTINCT lang FROM chan_lang;")

        self.langs = self.cur.fetchall()
        self.lang_sel = ""

        for i in range(len(self.langs)):
            self.langs[i] = self.langs[i][0]

        self.cur.execute("SELECT DISTINCT region FROM satellite;")

        self.regions = self.cur.fetchall()

        for i in range(len(self.regions)):
            self.regions[i] = self.regions[i][0]

        print(self.regions)

        # pos search
        # self.cur.execute(
        #    "SELECT  name FROM satellite WHERE CAST ( pos AS float) = 177.0 AND SUBSTRING(pos, -1) = 'W';"
        # )

        self.title("Tv Satellites")
        self.geometry(
            "1400x850"
            + "+"
            + str(int((self.winfo_screenwidth() - 1400) / 2))
            + "+"
            + str(int((self.winfo_screenheight() - 850) / 2))
        )

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(
            self.navigation_frame,
            text="Tv Sattelite",
            compound="left",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.login_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Login",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.login_button_event,
        )
        self.login_button.grid(row=1, column=0, sticky="ew")

        self.signup_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Signup",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.signup_button_event,
        )
        self.signup_button.grid(row=2, column=0, sticky="ew")

        self.satellites_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Satellites",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.satellites_button_event,
        )
        self.satellites_button.grid(row=3, column=0, sticky="ew")
        self.satellites_button.grid_forget()

        self.viewable_channels_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Viewable channels",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.viewable_channels_button_event,
        )
        self.viewable_channels_button.grid(row=4, column=0, sticky="ew")
        self.viewable_channels_button.grid_forget()

        self.top_5_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Top 5",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.top_5_button_event,
        )
        self.top_5_button.grid(row=5, column=0, sticky="ew")
        self.top_5_button.grid_forget()

        self.channels_button = ctk.CTkButton(
            self.navigation_frame,
            corner_radius=0,
            height=40,
            border_spacing=10,
            text="Channels",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="w",
            command=self.channels_button_event,
        )
        self.channels_button.grid(row=6, column=0, sticky="ew")
        self.channels_button.grid_forget()

        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.navigation_frame,
            values=["System", "Light", "Dark"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create satellites frame

        self.login_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.login_frame.grid_columnconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(1, weight=1)
        self.login_frame.grid_columnconfigure(2, weight=1)

        self.user_login_entry = ctk.CTkEntry(
            self.login_frame,
            placeholder_text="Username",
        )
        self.user_login_entry.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.pass_login_entry = ctk.CTkEntry(
            self.login_frame,
            show="*",
            placeholder_text="Password",
        )
        self.pass_login_entry.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.login_check_button = ctk.CTkButton(
            self.login_frame,
            text="Login",
            compound="bottom",
            anchor="w",
            command=lambda: self.login_check_action(
                str(self.user_login_entry.get()), str(self.pass_login_entry.get())
            ),
        )
        self.login_check_button.grid(row=3, column=1, padx=20, pady=10, sticky="w")
        self.login_signup_button = ctk.CTkButton(
            self.login_frame,
            text="Signup",
            compound="bottom",
            anchor="w",
            command=lambda: self.select_frame_by_name("signup"),
        )
        self.login_signup_button.grid(row=4, column=1, padx=20, pady=10, sticky="w")
        self.singup_statement_lgn = ctk.CTkLabel(
            self.login_frame, text="Create new account?"
        )
        self.singup_statement_lgn.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        # create second frame
        self.signup_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.signup_frame.grid_columnconfigure(0, weight=1)
        self.signup_frame.grid_columnconfigure(1, weight=1)
        self.signup_frame.grid_columnconfigure(2, weight=1)

        self.user_signup_entry = ctk.CTkEntry(
            self.signup_frame,
            placeholder_text="Username",
        )
        self.user_signup_entry.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.pass_signup_entry = ctk.CTkEntry(
            self.signup_frame,
            show="*",
            placeholder_text="Password",
        )
        self.pass_signup_entry.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.pass_c_signup_entry = ctk.CTkEntry(
            self.signup_frame,
            show="*",
            placeholder_text="Confirm Password",
        )
        self.pass_c_signup_entry.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.email_signup_entry = ctk.CTkEntry(
            self.signup_frame,
            placeholder_text="Email",
        )
        self.email_signup_entry.grid(row=5, column=0, padx=20, pady=10, sticky="w")
        self.region_signup_menu = ctk.CTkOptionMenu(
            self.signup_frame, values=self.regions
        )
        self.region_signup_menu.set("Region")
        self.region_signup_menu.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        self.location_signup_entry = ctk.CTkEntry(
            self.signup_frame,
            placeholder_text="Location",
        )
        self.location_signup_entry.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        self.birthdate_signup_entry = ctk.CTkEntry(
            self.signup_frame,
            placeholder_text="yyyy-mm-dd",
        )
        self.birthdate_signup_entry.grid(row=8, column=0, padx=20, pady=10, sticky="w")
        self.gender_signup_menu = ctk.CTkOptionMenu(
            self.signup_frame,
            values=["Male", "Female"],
        )
        self.gender_signup_menu.set("Gender")
        self.gender_signup_menu.grid(row=9, column=0, padx=20, pady=10, sticky="w")
        self.signup_login_button = ctk.CTkButton(
            self.signup_frame,
            text="Login",
            compound="bottom",
            anchor="w",
            command=lambda: self.select_frame_by_name("login"),
        )

        self.signup_login_button.grid(row=10, column=1, padx=20, pady=10, sticky="w")

        self.signup_check_button = ctk.CTkButton(
            self.signup_frame,
            text="Signup",
            compound="bottom",
            anchor="w",  #  user pass_ pass_c email region location birthdate gender
            command=lambda: self.signup_check_action(
                self.user_signup_entry.get(),
                self.pass_signup_entry.get(),
                self.pass_c_signup_entry.get(),
                self.email_signup_entry.get(),
                self.region_signup_menu.get(),
                self.location_signup_entry.get(),
                self.birthdate_signup_entry.get(),
                self.gender_signup_menu.get(),
            ),
        )

        self.signup_check_button.grid(row=9, column=1, padx=20, pady=10, sticky="w")

        self.login_statement_sgn = ctk.CTkLabel(
            self.signup_frame, text="Already have an account?"
        )
        self.login_statement_sgn.grid(row=10, column=0, padx=20, pady=10, sticky="w")

        # create third frame
        self.satellites_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        # create 4th frame
        self.viewable_channels_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.pos_entry = ctk.CTkEntry(
            self.viewable_channels_frame, placeholder_text="position"
        )

        self.pos_entry.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        self.pos_check_button = ctk.CTkButton(
            self.viewable_channels_frame, text="Search", command=self.pos_action
        )
        self.pos_check_button.grid(row=2, column=0, sticky="ew", pady=20)

        self.only_fave_box = ctk.CTkCheckBox(
            self.viewable_channels_frame, text="Only favorites"
        )
        self.only_fave_box.grid(row=1, column=0, sticky="ew", pady=20)

        # create 5th frame
        self.top_5_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.radio_var = ctk.IntVar(value=0)
        self.networks_btn = ctk.CTkRadioButton(
            self.top_5_frame,
            text="Networks",
            command=lambda: self.top_5_radio_command("networks"),
            radiobutton_width=20,
            radiobutton_height=19,
            variable=self.radio_var,
            value=1,
        )
        self.networks_btn.grid(row=0, column=0, sticky="w")

        self.rockets_btn = ctk.CTkRadioButton(
            self.top_5_frame,
            text="Rockets",
            command=lambda: self.top_5_radio_command("rockets"),
            radiobutton_width=20,
            radiobutton_height=19,
            variable=self.radio_var,
            value=2,
        )
        self.rockets_btn.grid(row=1, column=0, sticky="w")

        self.satellites_btn = ctk.CTkRadioButton(
            self.top_5_frame,
            text="Satellites",
            command=lambda: self.top_5_radio_command("satellites"),
            radiobutton_width=20,
            radiobutton_height=19,
            variable=self.radio_var,
            value=3,
        )
        self.satellites_btn.grid(row=2, column=0, sticky="w")

        self.channels_btn = ctk.CTkRadioButton(
            self.top_5_frame,
            text="channels",
            command=lambda: self.langs_menu_top_5.grid(row=4, column=0, sticky="w"),
            radiobutton_width=20,
            radiobutton_height=19,
            variable=self.radio_var,
            value=4,
        )
        self.channels_btn.grid(row=3, column=0, sticky="w")
        self.var = ""
        self.langs_menu_top_5 = ctk.CTkOptionMenu(
            self.top_5_frame, values=self.langs, command=self.menu_command
        )
        self.langs_menu_top_5.set("Select Language")

        self.langs_menu_top_5.grid_forget()

        # create 6th frame
        self.channels_frame = ctk.CTkFrame(
            self, corner_radius=0, fg_color="transparent"
        )

        self.var = ""
        self.langs_menu_6th = ctk.CTkOptionMenu(
            self.channels_frame,
            values=self.langs,
            command=lambda event: self.menu_command_6th(
                self.langs_menu_6th.get(),
                self.region_menu_6th.get(),
                self.sats_6th.get(),
                self.hs_6th.get(),
            ),
        )
        self.langs_menu_6th.set("Select Language")

        self.langs_menu_6th.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.region_menu_6th = ctk.CTkOptionMenu(
            self.channels_frame,
            values=self.regions,
            command=lambda event: self.menu_command_6th(
                self.langs_menu_6th.get(),
                self.region_menu_6th.get(),
                self.sats_6th.get(),
                self.hs_6th.get(),
            ),
        )
        self.region_menu_6th.set("Select Region")

        self.region_menu_6th.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.sats_6th = ctk.CTkOptionMenu(
            self.channels_frame,
            values=self.sats,
            command=lambda event: self.menu_command_6th(
                self.langs_menu_6th.get(),
                self.region_menu_6th.get(),
                self.sats_6th.get(),
                self.hs_6th.get(),
            ),
        )
        self.sats_6th.set("Select Satellite")

        self.sats_6th.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.hs_6th = ctk.CTkOptionMenu(
            self.channels_frame,
            values=["HD", "SD"],
            command=lambda event: self.menu_command_6th(
                self.langs_menu_6th.get(),
                self.region_menu_6th.get(),
                self.sats_6th.get(),
                self.hs_6th.get(),
            ),
        )
        self.hs_6th.set("Select HD/SD")

        self.hs_6th.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # select default frame
        self.select_frame_by_name("login")

    def menu_command_6th(self, lang, region, sat, hs):
        querey = (
            """SELECT C.name as Channel, S.region as Region, S.name as Satellite, C.vid_encode as Encoding, CL.lang as Language"""
            + """
        FROM channels C LEFT JOIN chan_sat CS
        ON C.name = CS.channel_name 
        LEFT JOIN satellite S
        ON CS.sat_name = S.name
        LEFT JOIN chan_lang CL
        ON C.name = CL.name"""
        )

        if "Select" not in lang:
            querey = (
                querey
                + """
            WHERE CL.lang = '"""
                + lang
                + """'"""
                if "WHERE" not in querey
                else querey
                + """
            AND CL.lang = '"""
                + lang
                + """'"""
            )
        if "Select" not in region:
            querey = (
                querey
                + """
            WHERE S.region = '"""
                + region
                + """'"""
                if "WHERE" not in querey
                else querey
                + """
            AND S.region = '"""
                + region
                + """'"""
            )
        if "Select" not in sat:
            querey = (
                querey
                + """
            WHERE S.name = '"""
                + sat
                + """'"""
                if "WHERE" not in querey
                else querey
                + """
            AND S.name = '"""
                + sat
                + """'"""
            )
        if "Select" not in hs:
            querey = (
                querey
                + """
            WHERE C.vid_encode LIKE '%"""
                + hs
                + """%'"""
                if "WHERE" not in querey
                else querey
                + """
            AND C.vid_encode LIKE '%"""
                + hs
                + """%'"""
            )
            self.refresh(
                """channels C LEFT JOIN chan_sat CS
        ON C.name = CS.channel_name 
        LEFT JOIN satellite S
        ON CS.sat_name = S.name
        LEFT JOIN chan_lang CL
        ON C.name = CL.name""",
                self.channels_frame,
                0,
                querey,
            )

    def menu_command(self, event):
        self.lang_sel = self.langs_menu_top_5.get()
        self.top_5_radio_command("channels")

    def top_5_radio_command(self, btn):
        querey = ""
        if btn == "networks":
            self.langs_menu_top_5.set("Select Language")
            self.langs_menu_top_5.grid_forget()
            querey = """
            SELECT CS.prov_pack as "provider/package", ROUND(AVG(DISTINCT Nos.num_of_sats),2) AS "average of satellites"
            FROM chan_sat CS
            INNER JOIN (
                SELECT channel_name, COUNT(DISTINCT sat_name) AS num_of_sats
                FROM chan_sat
                GROUP BY channel_name
            ) AS Nos ON CS.channel_name = Nos.channel_name
            WHERE CS.prov_pack IS NOT NULL
            GROUP BY CS.prov_pack ORDER BY `average of satellites` desc LIMIT 5 
            """
        elif btn == "rockets":
            self.langs_menu_top_5.set("Select Language")
            self.langs_menu_top_5.grid_forget()
            querey = """
            SELECT launch_rkt as Rocket, COUNT(DISTINCT(name)) as "Number of satellites" FROM satellite
            WHERE launch_rkt IS NOT NULL
            GROUP BY launch_rkt ORDER BY `Number of satellites` desc LIMIT 5 
            """
        elif btn == "satellites":
            self.langs_menu_top_5.set("Select Language")
            self.langs_menu_top_5.grid_forget()
            querey = """
            SELECT 
            S.name, 
            COUNT(DISTINCT CS.channel_name) AS chn, 
            launch_date AS date,
            ROUND(COUNT(DISTINCT CS.channel_name) / 
                NULLIF(DATEDIFF(CURRENT_DATE(), S.launch_date), 0), 2) AS growth
        FROM 
            satellite S 
        LEFT JOIN 
            chan_sat CS ON S.name = CS.sat_name
        GROUP BY 
            S.name ORDER BY `growth` desc LIMIT 5 
            """
        elif btn == "channels":
            self.langs_menu_top_5.grid(row=4, column=0, sticky="w")
            querey = (
                """
            SELECT CL.lang as Language, CS.channel_name as Channel, COUNT(CS.sat_name) as "number of satellites"
            FROM chan_lang CL LEFT JOIN chan_sat CS 
            ON CL.name = CS.channel_name
            WHERE CL.lang = '"""
                + self.langs_menu_top_5.get()
                + """'
GROUP BY `CS`.channel_name
ORDER BY `number of satellites` desc LIMIT 5  
            """
            )

        self.refresh("chan_sat", self.top_5_frame, -1, querey)

    def pos_action(self):
        pos_regex = r"^[0-9]{1,3}[\.[0-9]{2}]?\°?[E|W|e|w]$"
        number = -2 if ("°" in self.pos_entry.get()) else -1
        if re.match(pos_regex, self.pos_entry.get()):
            if self.only_fave_box.get() == 0:
                # SELECT DISTINCT channel_name as 'channel_name Name', S.name as 'Satellite Name', S.pos as position FROM chan_sat CS LEFT JOIN satellite S ON CS.sat_name = S.name WHERE (CAST ( S.pos AS float) > 167
                # AND CAST ( S.pos AS float) < 187) AND SUBSTRING(pos, -1) = 'W'
                #
                querey = (
                    """SELECT DISTINCT channel_name as 'channel_name Name', S.name as 'Satellite Name', S.pos as position 
                        FROM chan_sat CS
                        LEFT JOIN satellite S ON CS.sat_name = S.name
                        WHERE (CAST(S.pos AS float) > """
                    + str(float(self.pos_entry.get()[:number]) - 10)
                    + " AND CAST(S.pos AS float) < "
                    + str(float(self.pos_entry.get()[:number]) + 10)
                    + ") AND SUBSTRING(pos, -1) = '"
                    + self.pos_entry.get()[-1].upper()
                    + "'"
                )
            else:
                querey = (
                    "SELECT DISTINCT FC.channel_name as 'channel_name Name', S.name as 'Satellite Name', S.pos as position, CS.frequency as Frequency, C.encryption as Encryption FROM fave_channel FC LEFT JOIN chan_sat CS ON FC.channel_name = CS.channel_name LEFT JOIN channels C ON C.name = CS.channel_name LEFT JOIN satellite S ON CS.sat_name = S.name WHERE (CAST(S.pos AS float) > "
                    + str(float(self.pos_entry.get()[:number]) - 10)
                    + " AND CAST(S.pos AS float) < "
                    + str(float(self.pos_entry.get()[:number]) + 10)
                    + ") AND SUBSTRING(pos, -1) = '"
                    + self.pos_entry.get()[-1].upper()
                    + "' AND FC.username = '"
                    + self.user
                    + "'"
                )
            print(querey)
            self.refresh(
                "channel",
                self.viewable_channels_frame,
                0,
                querey,
            )

    def signup_check_action(
        self, user, pass_, pass_c, email, region, location, birthdate, gender
    ):
        if len(user) < 2:
            print("username must have at least two characters")
            return
        self.cur.execute("SELECT username FROM user WHERE username = '" + user + "';")

        if len(self.cur.fetchall()) != 0:
            print("error: username exists")
            return
        if len(pass_) < 5:
            print("username must have at least 5 characters")
            return
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        if pass_ == pass_c:
            print("pass correct")
            if re.match(email_regex, email):
                print("email correct")
                # user, pass_, pass_c, email, region, location, birthdate, gender
                self.cur.execute(
                    "INSERT INTO user (username, pass, email, region, location, birthdate, gender) VALUES "
                    + str((user, pass_, email, region, location, birthdate, gender))
                    + ";"
                )
                self.conn.commit()
                self.user = user
                self.satellites_button.grid(row=0, column=0, sticky="ew")
                self.viewable_channels_button.grid(row=1, column=0, sticky="ew")
                self.top_5_button.grid(row=2, column=0, sticky="ew")
                self.channels_button.grid(row=3, column=0, sticky="ew")

                #
                self.login_button.grid_forget()
                self.signup_button.grid_forget()
                self.select_frame_by_name("satellites")

                pass
            else:
                print("email format wrong")
                return
            pass
        else:
            print("pass and pass confirm must be equal")
            return

    def refresh(self, table, frame, offset, querey):
        print(50 * "=")
        print(querey)
        try:
            self.cur.execute(
                "SELECT COUNT(*) AS total FROM (" + querey + ") AS subquery;"
            )

            count = self.cur.fetchall()[0][0]

            print(count)

            pages = count / 50
        except:
            pages = -1
            pass

        self.cur.execute(
            "SELECT region FROM user WHERE username = '" + self.user + "';"
        )
        region = self.cur.fetchall()[0][0]
        region = str.lower(region)
        try:
            self.cur.execute(querey + " LIMIT 50 OFFSET " + str(offset) + ";")
        except:
            self.cur.execute(querey + ";")

        print(50 * "=")

        # self.Frame.destroy()
        # self.Frame.grid

        try:
            self.Frame.grid_forget()
            self.Frame.destroy()
        except:
            pass

        self.Frame = ctk.CTkScrollableFrame(
            frame,
            orientation="both",
            scrollbar_button_color="grey30",
            bg_color="transparent",
            fg_color="transparent",
            height=780,
            width=1190,
        )
        self.Frame.grid(row=0, column=1, columnspan=10, rowspan=50)
        self.Frame.grid_columnconfigure(0, weight=1)
        self.Frame.grid_columnconfigure(1, weight=1)

        prev = ctk.CTkButton(
            self.Frame,
            text="Prev",
            command=lambda: self.refresh(table, frame, offset - 50, querey),
            width=15,
            fg_color="#5696b0",
            # fg_color="transparent",
        )
        if int(offset / 50) + 1 != 1 and offset != -1:
            prev.grid(row=0, column=0, padx=10, pady=5)

        next_ = ctk.CTkButton(
            self.Frame,
            text="Next",
            command=lambda: self.refresh(table, frame, offset + 50, querey),
            width=15,
            fg_color="#5696b0",
            # fg_color="transparent",
        )
        if int(offset / 50) + 1 != math.ceil(pages) and offset != -1:
            next_.grid(row=0, column=1, padx=10, pady=5)

        pages_statement = ctk.CTkLabel(
            self.Frame,
            text=(
                "Page " + str(int(offset / 50) + 1) + " of " + str(math.ceil(pages))
                if offset != -1
                else ""
            ),
        )
        pages_statement.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        print(50 * "=")
        print(querey + "this is the line")

        self.Headers = [description[0] for description in self.cur.description]
        self.headers = self.Headers.copy()
        for i in range(len(self.Headers)):
            if self.headers[i] == "profile":
                pass
            else:
                self.headers[i] = self.headers[i].replace("_", " ")
        self.RowsData = self.cur.fetchall()
        print(self.headers, self.RowsData)
        self.NumRows = len(self.RowsData)
        self.Entries = []

        if len(self.Headers) > 0:
            for col, header in enumerate(self.headers):
                self.label = ctk.CTkLabel(self.Frame, text=header)
                self.label.grid(row=0, column=col + 2, padx=10, pady=5)

        if len(self.RowsData) > 0:
            for row, row_data in enumerate(self.RowsData, start=1):
                for col, value in enumerate(row_data):
                    if "channel" in table:
                        print(50 * "channnnnnnn")
                        self.cur.execute(
                            'SELECT channel_name from fave_channel WHERE username = "'
                            + self.user
                            + '" AND channel_name = "'
                            + row_data[0]
                            + '";'
                        )

                        color = ""
                        if len(self.cur.fetchall()) < 1:
                            color = "transparent"
                        else:
                            color = ("#a8f0b4", "#576e5a")

                        fav = ctk.CTkButton(
                            self.Frame,
                            text="",
                            command=lambda chan=row_data[
                                0
                            ], temp=row: self.fave_command(
                                self.Frame, chan, temp, len(self.Headers) + 3
                            ),
                            width=15,
                            height=15,
                            image=ctk.CTkImage(
                                light_image=Image.open("fav.png"),
                                size=(15, 15),
                                dark_image=Image.open("favD.png"),
                            ),
                            bg_color="transparent",
                            fg_color=color,
                            hover_color="#c4c4c4",
                        )

                        fav.grid(
                            row=row,
                            column=len(self.Headers) + 3,
                            padx=10,
                            pady=5,
                            sticky="w",
                        )

                    entry = ctk.CTkEntry(self.Frame, width=100, state="normal")
                    if value is not None:
                        if self.headers[col] != "Encryption":
                            entry.insert(ctk.END, value)
                        elif len(value) > 2:
                            entry.insert(ctk.END, "Encrypted")
                        else:
                            entry.insert(ctk.END, "Free")

                    else:
                        if self.headers[col] != "Encryption":
                            pass
                        else:
                            entry.insert(ctk.END, "Free")
                    entry.configure(
                        state="disabled",
                        fg_color=("#bababa", "#262626"),
                    )
                    entry.grid(row=row, column=col + 2, padx=10, pady=5)
                    self.Entries.append(entry)

    def fave_command(self, frame, chan, row, col):
        print(
            "SELECT channel_name from fave_channel WHERE username = '"
            + self.user
            + "' AND channel_name = '"
            + chan
            + "';"
        )
        print(50 * "-")
        self.cur.execute(
            'SELECT channel_name from fave_channel WHERE username = "'
            + self.user
            + '" AND channel_name = "'
            + chan
            + '";'
        )

        color = ""
        if len(self.cur.fetchall()) < 1:
            self.cur.execute(
                "INSERT INTO fave_channel (username, channel_name) VALUES "
                + str((self.user, chan))
                + ";"
            )
            color = ("#a8f0b4", "#576e5a")
        else:
            self.cur.execute(
                'DELETE FROM fave_channel WHERE username = "'
                + self.user
                + '" AND channel_name = "'
                + chan
                + '";'
            )

            color = "transparent"

        frame.grid_slaves(row=row, column=col)[0].configure(fg_color=color)
        self.conn.commit()
        pass

    def login_check_action(self, user, pass_):
        print(user, pass_)
        self.cur.execute("SELECT username FROM user WHERE username = '" + user + "';")

        if len(self.cur.fetchall()) == 0:
            # error no user found
            print("error: no user found")
            return

        self.cur.execute("SELECT pass FROM user WHERE username = '" + user + "';")

        fetch = self.cur.fetchall()

        if pass_ == fetch[0][0]:
            print("logged in")
            self.user = user
            self.login_flag = True
            self.satellites_button.grid(row=0, column=0, sticky="ew")
            self.viewable_channels_button.grid(row=1, column=0, sticky="ew")
            self.top_5_button.grid(row=2, column=0, sticky="ew")
            self.channels_button.grid(row=3, column=0, sticky="ew")

            self.login_button.grid_forget()
            self.signup_button.grid_forget()
            self.select_frame_by_name("satellites")

        else:
            print("wrong password")

    def login_signup_action():
        pass

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.login_button.configure(
            fg_color=("gray75", "gray25") if name == "login" else "transparent"
        )
        self.signup_button.configure(
            fg_color=("gray75", "gray25") if name == "signup" else "transparent"
        )
        self.satellites_button.configure(
            fg_color=("gray75", "gray25") if name == "satellites" else "transparent"
        )
        self.viewable_channels_button.configure(
            fg_color=(
                ("gray75", "gray25") if name == "viewable_channels" else "transparent"
            )
        )
        self.top_5_button.configure(
            fg_color=("gray75", "gray25") if name == "top_5" else "transparent"
        )
        self.channels_button.configure(
            fg_color=("gray75", "gray25") if name == "channels" else "transparent"
        )

        # show selected frame
        if name == "login":
            self.login_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.login_frame.grid_forget()
        if name == "signup":
            self.signup_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.signup_frame.grid_forget()
        if name == "satellites":
            self.refresh(
                "satellite", self.satellites_frame, 0, "SELECT * FROM satellite"
            )
            self.satellites_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.satellites_frame.grid_forget()
        if name == "viewable_channels":
            self.viewable_channels_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.viewable_channels_frame.grid_forget()
        if name == "top_5":
            self.top_5_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.top_5_frame.grid_forget()
        if name == "channels":
            self.channels_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.channels_frame.grid_forget()

    def login_button_event(self):
        self.select_frame_by_name("login")

    def signup_button_event(self):
        self.select_frame_by_name("signup")

    def satellites_button_event(self):
        self.select_frame_by_name("satellites")

    def viewable_channels_button_event(self):
        self.select_frame_by_name("viewable_channels")

    def top_5_button_event(self):
        self.select_frame_by_name("top_5")

    def channels_button_event(self):
        self.select_frame_by_name("channels")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()
