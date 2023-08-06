import numpy as np

import plotly.graph_objs as go

import cgi
# Create instance of FieldStorage
form = cgi.FieldStorage()
forme = cgi.FieldStorage()
formee= cgi.FieldStorage()


class Polar_bec:
    # to use this librairy you must import nmpy like bellow: import numpy as np
    def __init__(self):

        global f, i
        f = []
        i = 0
        s = []

    def bec_cal( P, L):

        """

        :type P: object
        """
        # P is the ereasure probability
        # L is level of polarisation they start from one
        if L == 1:
            P1 = P * P
            P2 = P * (2 - P)

            context = {
                'P1': P1,
                'P2': P2,

            }
            f.append(P1)
            f.append(P2)
            #print("f is ", f)
            return (P1, P2)
        else:
            return (Polar_bec.bec_cal(P * P, L - 1), Polar_bec.bec_cal(P * (2 - P), L - 1))
    def input_p_n(self):
        p = float(input("\n\nPlease enter the ereasure probability:\n"))
        print(f'the ereasure probability is {p} \n')
        n = int(input("Please enter the code length:\n"))
        print(f'the code  length is {n}')
        return (p,n)
    def BEC(P,N):
        # N is the code length it must a power of two
        L = np.log2(N)

        Polar_bec.bec_cal(P,L)
        return f

    def BEC_graph(p,n):
    #this function plot the new ereasure probability
        Polar_bec.__init__(0)
        result = Polar_bec.BEC(p, n)

        i=1
        good = []
        bad= []
        index_good=[]
        index_bad = []

        for i in range(n):
                if ( result[i] < p ):
                    good.append(result[i])
                    index_good.append(i)

                else:
                    bad.append(result[i])
                    index_bad.append(i)

        print(f'after polarization we get {len(bad)} of bad channels :', bad)
        print(f'after polarization we get {len(good)} of good channels :', good)

        index = list(range(1, n + 1))

        p_initial_value = [p, p]
        n_initial_value = [0, n]
        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(x=index_good, y=good, showlegend=True, mode='markers',marker_color='IndianRed', opacity=1, name="good channels ",marker_size=8))

        fig2.add_trace(go.Scatter(x=index_bad, y=bad, showlegend=True, mode='markers', marker_color='LightSeaGreen',opacity=1, name="bad channels ", marker_size=8))

        fig2.add_trace(go.Scatter(x=n_initial_value, y=p_initial_value, showlegend=True, mode='lines', opacity=1,marker_line_width=2, name="initial ereasure probability "+str(p),line=dict(color='sandybrown', width=4)))
        fig2.update_xaxes(title_text="index channel")
        fig2.update_xaxes(title_font={"size": 25})
        # ***fig2.update_yaxes(title_text="BER and FER")
        # ***fig2.update_yaxes(title_text="BER and FER")
        fig2.update_yaxes(title_text="NEW EREASURE PROBABILITY")
        # fig2.update_yaxes(type="log")
        fig2.update_yaxes(title_font={"size": 25})
        fig2.update_yaxes(showgrid=True)
        fig2.update_traces(textposition='top center')
        fig2.update_layout(height=800,title_text="the new ereasure probability for " + " N=" + str(n) + " and p =" + str(p))
        # fig2.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.90))
        # fig2.update_traces(mode='markers', marker_line_width=2, marker_size=8)
        fig2.add_annotation(x=n/2, y=p+(1-p)/2,
                            text="bad channels",showarrow=False,
                            font=dict(family="sans serif",
                            size=24,color="LightSeaGreen"),arrowhead=1)
        fig2.add_annotation(x=n/2, y=p-(1-p)/2,
                            text="good channels",showarrow=False,
                            font=dict(family="sans serif",
                            size=24,color="IndianRed"),arrowhead=1)

        fig2.add_annotation(x=n / 2, y=p-0.025,
                        text="initial ereasure probability "+str(p), showarrow=False,
                        font=dict(family="sans serif",
                                  size=24, color="sandybrown"), arrowhead=1)


        fig2.add_layout_image(
            dict(
                source="https://miro.medium.com/max/534/1*lo0ScwNgbgDtlhqHawrECw.png",
                xref="x",
                yref="y",
                x=0.1,
                y=1,
                sizex=1.75,
                sizey=0.25,
                sizing="stretch",
                opacity=0.5,
                layer="below")
        )
        # Set templates
        #fig2.update_layout(template="plotly_white")


        fig2.show()