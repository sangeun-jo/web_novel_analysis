from django.shortcuts import render
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import font_manager, rc
import re, io
import urllib, base64
from web_novel_analysis.base import get_weeks_data 
from web_novel_analysis.base import wordcloud, get_tags, get_keys

def home(request): 
    
    filtered = get_weeks_data(7); 
    w_keyword = get_tags(filtered) 
    top_ten = get_keys(filtered, 10)
    return render(request, 'index.html', {'wordcloud':wordcloud(w_keyword), 'top_keys':top_ten})
