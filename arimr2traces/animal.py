# -*- coding: utf-8 -*-
import csv
from datetime import datetime
from typing import List

DATA_NOT_FETCHED = 'dane niepobrane'
ANIMAL_ID_MISMATCH = 'niepoprawny nr zwierzaka'
ANIMAL_NOT_FOUND = 'nieznaleziono zwierzaka'
ANIMAL_OK = 'ok'

ANIMAL_SPECIES_CATTLE = 'bydło'
ANIMAL_SPECIES_SHEEP = 'owce'

ANIMAL_SEX_MALE = 'XY - Samiec'
ANIMAL_SEX_FEMALE = 'XX - Samica'


class Animal:
    """
    object representing Animal properties found on ARiMR webpage

    """
    def __init__(self, animal_id):
        self.animal_id = animal_id
        self.past_animal_id = ''
        self.id_new_earring = ''
        self.species = ''
        self.birth_date = ''
        self.sex = ''
        self.breed = ''
        self.typ_uzyt = ''
        self.mother_id = ''
        self.purchase_from_ue_date = ''
        self.country_of_origin = ''
        self.status = ''
        self.status_epizoot = ''
        self.remarks = ''
        self.passport_id = ''
        self.passport_status = ''

        self.events_list : List[AnimalEvent] = list()
        self.process_status = DATA_NOT_FETCHED
        self.herd_id = ''

    def set_data(self, past_animal_id, id_ne_earring, species, birth_date, sex, breed, typ_uzyt, mother_id,
                 purchase_from_ue_date, panstwo_poch, status, status_epizoot, remarks, passport_id, passport_status, nr_stada):
        self.past_animal_id = past_animal_id
        self.id_new_earring = id_ne_earring
        self.species = species
        self.birth_date = birth_date
        self.sex = sex
        self.breed = breed
        self.typ_uzyt = typ_uzyt
        self.mother_id = mother_id
        self.purchase_from_ue_date = purchase_from_ue_date
        self.country_of_origin = panstwo_poch
        self.status = status
        self.status_epizoot = status_epizoot
        self.remarks = remarks
        self.passport_id = passport_id.replace(' ', '')
        self.passport_status = passport_status
        self.herd_id = nr_stada

    def age_in_months(self, now=datetime.now()):
        if not self.birth_date:
            return ''
        dob = datetime.strptime(self.birth_date, "%Y-%m-%d").date()
        # https://stackoverflow.com/a/16614616/857893
        years = now.year - dob.year
        months = now.month - dob.month
        if now.day < dob.day:
            months -= 1
            while months < 0:
                months += 12
                years -= 1
        #
        # tylko w miesiacch
        #
        return years*12+months

    def get_traces_sex(self):
        return 'female' if self.sex == ANIMAL_SEX_FEMALE else 'male'

    def get_animal_events_states_text(self):
        return ', '.join([animal_event.stan_zdarzenia for animal_event in self.events_list])


class AnimalEvent:
    """
    object representing one event from animal history
    """
    def __init__(self, typ_zdarzenie, nr_w_oznakowaniu, nr_siedziby, data_zdarzenia, stan_zdarzenia,
                 nr_siedziby_stad_kompl, uwagi):
        self.event_type = typ_zdarzenie
        self.nr_w_oznakowaniu = nr_w_oznakowaniu
        self.nr_siedziby = nr_siedziby
        self.data_zdarzenia = data_zdarzenia
        self.stan_zdarzenia = stan_zdarzenia
        self.nr_siedziby_stad_kompl = nr_siedziby_stad_kompl
        self.uwagi = uwagi


def read_list_of_ids(file_name):
    """
    Reads text file with simple list of animal IDsm like:
    PL00111234567
    PL00111234568
    ...

    :param file_name:
    :return: list
    """
    ids_list = list()
    with open(file_name) as csvfile:
        csvreader = csv.DictReader(csvfile, fieldnames=['animal_id'])
        for row in csvreader:
            ids_list.append(row['animal_id'].strip())
    return ids_list
