#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 15 19:27:23 2021

@author: oscar
"""

import ast
import traceback
from sys import exc_info

import pandas as pd

pd.options.mode.chained_assignment = None


ERR_SYS = "system error: "

POSTS_COLUMNS_FB = ["post_from", "post_id", "created_time", "permalink_url"]
EMPTY_COLUMNS_FB = [
    "post_id",
    "created_time",
    "name",
    "post_impressions",
    "post_impressions_unique",
    "post_impressions_paid",
    "post_impressions_paid_unique",
    "post_impressions_fan",
    "post_impressions_fan_unique",
    "post_impressions_fan_paid",
    "post_impressions_fan_paid_unique",
    "post_impressions_organic",
    "post_impressions_organic_unique",
    "post_impressions_viral",
    "post_impressions_viral_unique",
    "post_impressions_nonviral",
    "post_impressions_nonviral_unique",
    "post_impressions_by_story_type",
    "post_impressions_by_story_type_unique",
]

POSTS_COLUMNS_IG = ["owner_username", "shortcode", "date_local", "url"]
EMPTY_COLUMNS_IG = [
    "shortcode",
    "date_local",
    "name",
    "impressions",
    "reach",
    "engagement",
]


class ReachFaceInst:
    """
    This class match posts to reach
    """

    def __init__(self, df_post, df_ins, social_n="fb", url=False):
        """
        This method joins the information of publications with the information of insights,
        reads the information of several brands, in list format is important

        Parameters
        ----------
        df_post : TYPE dataframe
            DESCRIPTION. posts information
        df_ins : TYPE dataframe
            DESCRIPTION. insights information
        social_n : TYPE string
            DESCRIPTION. indicates social network, 'fb': Facebook, 'ig': Instagram
        url : TYPE string
            DESCRIPTION. is True if load post url

        Returns
        -------
        None.

        """

        self.df_post = df_post
        self.df_ins = df_ins
        self.social_n = social_n
        self.url = url

    def reach(self):
        """
        joint informtion posts and insights

        Returns
        -------
        df_reach : TYPE dataframe
            DESCRIPTION. dataframe whit reach, brand, date and post_id

        """

        df_post = self.df_post
        df_ins = self.df_ins
        social_n = self.social_n
        url = self.url
        method_name = "reach Facebook Instagram"

        try:

            if social_n == "fb":
                if url:
                    EMPTY_COLUMNS_FB.append("permalink_url")

                EMPTY_COLUMNS = EMPTY_COLUMNS_FB
                POSTS_COLUMNS = POSTS_COLUMNS_FB
                POST_FROM = "post_from"
                ON = "post_id"
                NAME = "name"

                df_reach_empty = pd.DataFrame(columns=EMPTY_COLUMNS)

                if df_post[POST_FROM].isna().values.any():
                    df_post = df_post[df_post[POST_FROM].notna()]

                brand_name = df_post[POST_FROM].apply(lambda x: ast.literal_eval(x))
                name = []
                for i in range(len(df_post)):
                    temp_3 = brand_name.iloc[i][NAME]
                    name.append(temp_3)

                df_post = df_post[POSTS_COLUMNS]
                df_post = df_post.drop(columns="post_from")
                df_post[NAME] = name

            elif social_n == "ig":
                if url:
                    EMPTY_COLUMNS_IG.append("url")

                df_post = df_post.rename(columns={"owner_username": "name"})
                EMPTY_COLUMNS = EMPTY_COLUMNS_IG
                POSTS_COLUMNS = POSTS_COLUMNS_IG
                POST_FROM = "shortcode"
                ON = "shortcode"
                NAME = "name"

                df_reach_empty = pd.DataFrame(columns=EMPTY_COLUMNS)

                if df_post[POST_FROM].isna().values.any():
                    df_post = df_post[df_post[POST_FROM].notna()]

            else:
                print(f"{social_n} is not a valid value")

            df_reach = pd.merge(df_post, df_ins, on=ON, how="outer")
            df_reach = df_reach[EMPTY_COLUMNS]
            df_reach = df_reach.dropna().reset_index(drop=True)

        except KeyError as e_1:
            print("==========================================================")
            print(e_1)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_reach = df_reach_empty

        except AttributeError as e_2:
            print("==========================================================")
            print(e_2)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_reach = df_reach_empty

        except Exception as e_3:
            print("==========================================================")
            print(e_3)
            print("==========================================================")
            print(ERR_SYS + str(exc_info()[0]))
            print("==========================================================")
            print(f"Class: {self.__str__()}\nMethod: {method_name}")
            print("==========================================================")
            traceback.print_exc()

            df_reach = df_reach_empty

        return df_reach
