# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fastdtlmapper',
 'fastdtlmapper.angst',
 'fastdtlmapper.angst.model',
 'fastdtlmapper.bin',
 'fastdtlmapper.bin.OrthoFinder',
 'fastdtlmapper.bin.OrthoFinder.scripts_of',
 'fastdtlmapper.bin.OrthoFinder.tools',
 'fastdtlmapper.bin.angst.angst_lib',
 'fastdtlmapper.bin.angst.tree_lib',
 'fastdtlmapper.goea',
 'fastdtlmapper.scripts',
 'fastdtlmapper.util']

package_data = \
{'': ['*'],
 'fastdtlmapper.bin': ['mafft/*',
                       'mafft/mafftdir/bin/*',
                       'mafft/mafftdir/libexec/*'],
 'fastdtlmapper.bin.OrthoFinder.scripts_of': ['bin/*']}

install_requires = \
['biopython>=1.79,<2.0',
 'goatools>=1.1.6,<2.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'scipy>=1.7.1,<2.0.0']

entry_points = \
{'console_scripts': ['FastDTLgoea = fastdtlmapper.scripts.FastDTLgoea:main',
                     'FastDTLmapper = '
                     'fastdtlmapper.scripts.FastDTLmapper:main']}

setup_kwargs = {
    'name': 'fastdtlmapper',
    'version': '0.2.1',
    'description': 'Fast genome-wide DTL(Duplication-Transfer-Loss) event mapping tool',
    'long_description': "# (Under Construction) FastDTLmapper: Fast genome-wide DTL event mapper  \n\n![Python3](https://img.shields.io/badge/Language-Python_3.7_|_3.8_|_3.9-steelblue)\n![OS](https://img.shields.io/badge/OS-Linux-steelblue)\n![License](https://img.shields.io/badge/License-GPL3.0-steelblue)\n[![Latest PyPI version](https://img.shields.io/pypi/v/fastdtlmapper.svg)](https://pypi.python.org/pypi/fastdtlmapper)\n[![Downloads](https://static.pepy.tech/personalized-badge/fastdtlmapper?period=month&units=international_system&left_color=grey&right_color=orange&left_text=Downloads)](https://pepy.tech/project/fastdtlmapper)  \n![CI workflow](https://github.com/moshi4/FastDTLmapper/actions/workflows/CI.yml/badge.svg)\n[![codecov](https://codecov.io/gh/moshi4/FastDTLmapper/branch/main/graph/badge.svg?token=ZJ8D747JUY)](https://codecov.io/gh/moshi4/FastDTLmapper)\n\n## Table of contents\n\n- [Overview](#overview)\n- [Install](#install)\n- [Pipeline Summary](#pipeline-summary)\n- [Command Usage](#command-usage)\n- [Output Contents](#output-contents)\n\n## Overview\n\nGene gain/loss is considered to be one of the most important evolutionary processes\ndriving adaptive evolution, but it remains largely unexplored.\nTherefore, to investigate the relationship between gene gain/loss and adaptive evolution\nin the evolutionary process of organisms, I developed a software pipeline **FastDTLmapper**\nwhich automatically estimates and maps genome-wide gene gain/loss.  \nFastDTLmapper takes two inputs, 1. Species tree (Newick format) 2. Genomic CDSs (Fasta|Genbank format),\nand performs genome-wide mapping of DTL(Duplication-Transfer-Loss) events by\nDTL reconciliation of species tree and gene trees.  \n\n![demo_all_gain_loss_map.png](https://github.com/moshi4/FastDTLmapper/wiki/images/demo_all_gain_loss_map.png)  \n**Fig. Genome-wide gain/loss map result example (all_gain_loss_map.png)**  \nEach nodes gain/loss data is mapped in following format (*NodeID | GeneCount [gain=GainCount los=LossCount]*)  \nMap data is embeded in newick format bootstrap value field and user can visualize using [SeaView](http://doua.prabi.fr/software/seaview).\n\n## Install\n\nFastDTLmapper is implemented in **Python3(>=3.7)** and runs on **Linux** (Tested on Ubuntu20.04).  \n\nInstall PyPI stable version with pip:\n\n    pip install fastdtlmapper\n\nInstall latest development version with pip:\n\n    pip install git+git://github.com/moshi4/FastDTLmapper.git\n\n### Dependencies\n\nAll of the following dependencies are packaged in **src/fastdtlmapper/bin** directory.  \n\n- [OrthoFinder](https://github.com/davidemms/OrthoFinder)  \n  Orthology inference tool\n- [mafft](https://mafft.cbrc.jp/alignment/software/)  \n  Sequences alignment tool\n- [trimal](http://trimal.cgenomics.org/)  \n  Alignment sequences trim tool\n- [IQ-TREE](http://www.iqtree.org/)  \n  Phylogenetic tree reconstruction tool\n- [AnGST](https://github.com/almlab/angst)  \n  DTL reconciliation tool (Requires Python 2.X to run)\n- [parallel](https://www.gnu.org/software/parallel/)  \n  Job parallelization tool (Requires Perl to run)\n\n## Pipeline Summary\n\n1. Grouping ortholog sequences using OrthoFinder\n2. Align each OG(Ortholog Group) sequences using mafft\n3. Trim each OG alignment using trimal\n4. Reconstruct each OG gene tree using IQ-TREE\n5. Species tree & each OG gene tree DTL reconciliation using AnGST\n6. Aggregate and map genome-wide DTL reconciliation result\n\n## Command Usage\n\n### Run Command\n\n    FastDTLmapper -i [fasta|genbank directory] -t [species tree file] -o [output directory]\n\n### Options\n\n    -h, --help           show this help message and exit\n    -i , --indir         Input Fasta(*.fa|*.faa|*.fasta), Genbank(*.gb|*.gbk|*.genbank) directory\n    -t , --tree          Input rooted species tree file (Newick format)\n    -o , --outdir        Output directory\n    -p , --process_num   Number of processor (Default: MaxProcessor - 1)\n    --dup_cost           Duplication event cost (Default: 2)\n    --los_cost           Loss event cost (Default: 1)\n    --trn_cost           Transfer event cost (Default: 3)\n    --inflation          MCL inflation parameter (Default: 3.0)\n    --timetree           Use species tree as timetree (Default: off)\n    --rseed              Number of random seed (Default: 0)\n\n#### Input Limitation\n\n- fasta or genbank files (--indir option)  \n  Following characters cannot be included in file name '_', '-', '|', '.'\n- species tree file (--tree option)  \n  Species name in species tree must match fasta or genbank file name\n\n#### Timetree Option\n\nIf user set this option, input species tree must be ultrametric tree.  \n--timetree enable AnGST timetree option below (See [AnGST manual](<https://github.com/almlab/angst/blob/master/doc/manual.pdf>) for details).  \n> If the branch lengths on the provided species tree represent times,\n> AnGST can restrict the set of possible inferred gene transfers to\n> only those between contemporaneous lineages  \n\n### Example Command\n\n    FastDTLmapper -i ./example/fasta/ -t ./example/species_tree.nwk -o ./fastdtlmapper_result\n\n## Output Contents\n\n### Output Top Directory\n\n| Top directory           | Contents                                                     |\n| ----------------------- | ------------------------------------------------------------ |\n| 00_user_data            | Formatted user input fasta and tree files                    |\n| 01_orthofinder          | OrthoFinder raw output results                               |\n| 02_dtl_reconciliation   | Each OG(Ortholog Group) DTL reconciliation result            |\n| 03_aggregate_map_result | Genome-wide DTL reconciliation aggregated and mapped results |\n| log                     | Config log and command log files                                 |\n\n### Output Directory Structure & Files\n\n    .\n    ├── 00_user_data/  -- User input data\n    │\xa0\xa0 ├── fasta/     -- Formatted fasta files\n    │\xa0\xa0 └── tree/      -- Formatted newick species tree files\n    │\n    ├── 01_orthofinder/  -- OrthoFinder raw output results\n    │\n    ├── 02_dtl_reconciliation/  -- Each OG(Ortholog Group) DTL reconciliation result\n    │\xa0\xa0 ├── OG0000000/\n    │\xa0\xa0 │   ├── OG0000000.fa                 -- OG fasta file\n    │\xa0\xa0 │   ├── OG0000000_aln.fa             -- OG alignment fasta file\n    │\xa0\xa0 │   ├── OG0000000_aln_trim.fa        -- Trimmed OG alignement fasta file\n    │\xa0\xa0 │   ├── OG0000000_dtl_map.nwk        -- OG DTL event mapped tree file\n    │\xa0\xa0 │   ├── OG0000000_gain_loss_map.nwk  -- OG Gain-Loss event mapped tree file\n    │\xa0\xa0 │   ├── angst/                       -- AnGST DTL reconciliation result\n    │\xa0\xa0 │   └── iqtree/                      -- IQ-TREE gene tree reconstruction result\n    │\xa0\xa0 │\n    │\xa0\xa0 ├── OG0000001/\n    │\xa0\xa0 . \n    │\xa0\xa0 . \n    │\xa0\xa0 └── OGXXXXXXX/\n    │\n    ├── 03_aggregate_map_result/  -- Genome-wide DTL reconciliation aggregated and mapped results\n    │\xa0\xa0 ├── all_dtl_map.nwk              -- Genome-wide DTL event mapped tree file\n    │\xa0\xa0 ├── all_gain_loss_map.nwk        -- Genome-wide Gain-Loss event mapped tree file\n    │\xa0\xa0 ├── all_og_node_event.tsv        -- All OG DTL event record file\n    │\xa0\xa0 ├── all_transfer_gene_count.tsv  -- All transfer gene count file\n    │\xa0\xa0 └── all_transfer_gene_list.tsv   -- All transfer gene list file\n    │\n    └── log/\n        ├── parallel_cmds/ -- Parallel run command log results\n        └── run_config.log -- Program run config log file\n",
    'author': 'moshi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/moshi4/FastDTLmapper/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
