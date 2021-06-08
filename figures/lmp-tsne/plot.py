import pickle

import fire
import matplotlib.pyplot as plt
from thesis import save_fig, set_aspect_ratio, setup_plotting


def load_data():
    # Data obtained from:
    # github.com/indy-lab/war-of-words-2/4-analysis/latent-features.ipynb
    with open('tsne-data.pkl', 'rb') as f:
        return pickle.load(f)


def plot_tsne(ax):
    # Load data.
    data = load_data()
    idx = data['indices']
    embed = data['embedding']
    doss_refs = data['dossier_references']

    # Define values of clusters.
    ref2cluster = {
        # Top-left: Environment and Communications
        'A8-0483-2018': 'ec',  # Low carbon benchmarks and positive carbon impact benchmarks
        'ENVI-AD(2018)630616': 'ec',  # Low carbon benchmarks and positive carbon impact benchmarks
        'A8-0025-2015': 'ec',  # Amendment to the fuel quality directive and the renewable energy directive (Indirect Land Use Change)
        'A8-0037-2018': 'ot',  # Establishing the European Defence Industrial Decelopment Programme aiming at supporting the competitiveness and innovative capacity of the EU defence industry
        'A8-0305-2017': 'ec',  # Body of European Regulators for Electronic Communications
        'A8-0068-2019': 'ec',  # Justice programme
        'A8-0318-2017': 'ec',  # European Electronic Communications Code (Recast)
        'A8-0313-2017': 'ec',  # Protection of individuals with regard to the processing of personal data by the Union institutions, bodies, offices and agencies and on the free movement of such data
        'A8-0438-2018': 'ec',  # Re-use of public sector information (recast)
        'A8-0288-2015': 'ec',  # Zootechnical and genealogical conditions for trade in and imports into the Union of breeding animals and their germinal products
        'A8-0363-2018': 'ec',  # Disclosures relating to sustainable investments and sustainability risks
        # Top-center cluster: Defense and Protection
        'A8-0199-2015': 'dp',  # Protection of undisclosed know-how and business information (trade secrets) against their unlawful acquisition, use and disclosure
        'A8-0412-2018': 'dp',  # Establishing the European Defence Fund
        'CULT-AD(2017)595592': 'dp',  # Rules on the exercise of copyright and related rights applicable to certain online transmissions of broadcasting organisations and retransmissions of telecision and radio programmes
        'A8-0442-2018': 'dp',  # Rules facilitating the use of financial and other information for the precention, detection, investigation or prosecution of certain criminal offences
        'A8-0057-2018': 'dp',  # Proposal for a Directive of the European Parliament and of the Council to empower the competition authorities of the Member States to be more effective enforcers and to ensure the proper functioning of the internal market
        'A8-0244-2016': 'dp',  # Establishing an EU common list of safe countries of origin for the purposes of common procedures for granting and withdrawing international protection
        'A8-0211-2017': 'ot',  # Financial rules applicable to the general budget of the Union
        'A8-0018-2018': 'dp',  # Establishing a centralised system for the identification of Member States holding conviction information on third country nationals and stateless persons (TCN) to supplement and support the European Criminal Records Information System (ECRIS-TCN system)
        'A8-0355-2018': 'dp',  # Transparent and predictable working conditions in the European Union
        'A8-0409-2018': 'ot',  # Establishing the Connecting Europe Facility
        'LIBE-AD(2018)620997': 'dp',  # Import of cultural goods
        # Top-right cluster: Investment and Decelopment
        'A8-0238-2016': 'id',  # Prospectus to be published when securities are offered to the public or admitted to trading
        'LIBE-AD(2017)604830': 'id',  # Copyright in the Digital Single Market
        'EMPL-AD(2015)549263': 'id',  # European Fund for Strategic Investments
        'A8-0227-2018': 'id',  # Increase of the financial envelope of the Structural Reform Support Programme and adapt its general objective
        'CULT-AD(2017)592366': 'id',  # Addressing geo-blocking and other forms of discrimination based on customers' nationality, place of residence or place of establishment within the internal market
        'A8-0198-2017': 'id',  # Extension of the duration of the European Fund for Strategic Investments as well as the introduction of technical enhancements for that Fund and the European Investment Advisory Hub
        'A8-0139-2015': 'id',  # European Fund for Strategic Investments
        'A8-0148-2015': 'ot',  # Personal protective equipment
        # Bottom-left cluster: Business and Innovation
        'A8-0295-2018': 'bi',  # Prudential supervision of investment firms
        'A8-0278-2018': 'bi',  # Pan-European Personal Pension Product (PEPP)
        'AGRI-AD(2017)604833': 'bi',  # Promotion of the use of energy from renewable sources (recast)
        'AFET-AD(2018)612300': 'bi',  # Establishing the European Defence Industrial Decelopment Programme aiming at supporting the competitiveness and innovative capacity of the EU defence industry
        'A8-0482-2018': 'bi',  # Establishing the InvestEU Programme
        'A8-0011-2019': 'bi',  # European Union macro-prudential oversight of the financial system and establishing a European Systemic Risk Board
    }

    colors = {
        'dp': 'C3',
        'bi': 'C1',
        'ec': 'C2',
        'id': 'C0',
        'ot': 'lightgray',
    }

    markers = {
        'dp': 'X',
        'bi': 's',
        'ec': 'v',
        'id': 'o',
        'ot': '.',
    }

    labels = [
        r'Environment \& Communications',
        r'Defense \& Protection',
        r'Investment \& Development',
        r'Business \& Innovation',
        r'Others',
    ]

    lines = dict()

    for i, (x, y) in zip(idx, embed):
        ref = doss_refs[i]
        cluster = ref2cluster[ref]
        line = ax.plot(
            x, y, color=colors[cluster], marker=markers[cluster], markersize=5
        )
        if cluster not in line:
            lines[cluster] = line[0]

    handles = [lines['ec'], lines['dp'], lines['id'], lines['bi'], lines['ot']]

    plt.legend(
        handles,
        labels,
        loc='best',
        frameon=True,
        # fontsize='x-small',
        labelspacing=0.2,
        #            bbox_to_anchor=(0.52,0.78)
    )
    # Change the marker size manually for both lines.
    # for handle in legend.legendHandles:
    #     handle._legmarker.set_markersize(4)

    plt.tick_params(
        axis='both',  # changes apply to the x-axis
        which='both',  # both major and minor ticks are affected
        bottom=False,  # ticks along the bottom edge are off
        left=False,  # tickcs on the left edge are off
        top=False,  # ticks along the top edge are off
        labelbottom=False,  # labels along the bottom edge are off
        labelleft=False,
    )  # labels along the bottom edge are off

    set_aspect_ratio(ax, 'golden')


def plot(save_as=None):
    setup_plotting(size='fraction')

    fig, ax = plt.subplots()
    plot_tsne(ax)

    if save_as is not None:
        save_fig(fig, save_as, tight=True)
    else:
        plt.show()


if __name__ == '__main__':
    fire.Fire(plot)
