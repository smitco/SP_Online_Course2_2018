# lesson 04 testing for mailroom metaprogramming
# implemented using pytest
# !/usr/bin/env python3


import os
import datetime
import mailroom_meta as m
import pytest
import sys
from unittest import mock


def test_donor_properties():
    d = m.Donor("JK Rowling", [8752])
    d.add(4862)
    assert d.total == (8752 + 4862)
    assert d.count == 2
    assert d.average == (8752 + 4862)/2
    
def test_donor_letter(capsys):
    d = m.Donor("Jim Halpert", [2685])
    print(d.get_letter_text())
    sys.stderr.write("error")
    out, err = capsys.readouterr()
    assert "Jim Halpert" and "2,685" in out
    
def test_add_donation():
    ad = m.AllDonors()
    ad.add_donation("Jim Carrey", 3425)
    assert "Jim Carrey" in ad.donors

# def test_add_donation_existing

def test_thank_yous(capsys):
    user_inputs = ["George Washington", "4295", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "George Washington" and "4,295" in out

def test_thank_yous_list_exit(capsys):
    user_inputs = ["List", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "George Washington" and "Exiting" in out

def test_thank_yous_donation_exit(capsys):
    user_inputs = ["James Bond", "exit", "list", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "Exiting" in out
        assert "James Bond" not in out   

def test_thank_yous_large_donation(capsys):
    user_inputs = ["James Bond", "42954356804343", "list", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "too large" in out
        assert "James Bond" not in out


def test_thank_yous_invalid_entry(capsys):
    user_inputs = ["James Bond", "sdhfdhfd", "list", "exit"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.thank_yous()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "Invalid entry" in out
        assert "James Bond" not in out

def test_get_report(capsys):
    ad = m.AllDonors()
    ad.load_data()
    ad.get_report()
    sys.stderr.write("error")
    out, err = capsys.readouterr()
    assert "Joey Tribbiani" in out
    assert "9,000.00" in out


def test_send_letters():
    ad = m.AllDonors()
    ad.add_donation("John Wick", 6483)
    ad.send_letters()
    current = datetime.datetime.now()
    date = [str(current.month), str(current.day), str(current.year)]
    current_date = "_".join(date)
    letter_name = ("John Wick" + " " + current_date + ".txt")
    test_file = open(letter_name, "r")
    assert "John Wick" and "6,483" in test_file.read()


def test_match(capsys):
    user_inputs = ["3000", "4000", "3"]
    with mock.patch("builtins.input", side_effect=user_inputs):
        ad = m.AllDonors()
        ad.load_data()
        ad.match()
        sys.stderr.write("error")
        out, err = capsys.readouterr()
        assert "6,500" in out
        assert "19,500" in out

def test_save_data():
    ad = m.AllDonors()
    ad.add_donation("Jason Bourne", 3247)
    ad.save_data()
    test_file = open("Donor_Data.txt", "r")
    assert "Jason Bourne" and "3247" in test_file.read()


def test_quit():
    with pytest.raises(SystemExit) as py_se:
        ad = m.AllDonors()
        ad.quit()
    assert py_se.type == SystemExit