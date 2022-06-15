# fluka_shower_scripts
In this repository are scripts to prepare the data from Fluka outputs. Fluka output consists in one file from a shower (usually a high energetic proton) that contains trzcking information of Kaon0 and charged Kaons, pion0 and charged pions and charged muons.

The file data_prep.py read the output fluka file:

  - Creates a unique_id for each particle. This helps to separate duplicates (particles that appeas more than once because are transported)
  - Creates two more DataFrame, one for the first step of the particle and another for the last step.
  - Generates three new columns for further analysis: icode_anc, unique_id_anc and line_anc.
  - Rewrite the three df into a root file with three trees: main, first, last. Where main contains all track info, first the initial step and last the end point.
