
# def show_io(*args):
#     fig = make_subplots(cols=1, rows=len(args),
#                         subplot_titles=['Input', 'Correct', 'Predicted', 'Difference'])
#     for a, arg in enumerate(args):
#         fig.add_trace(go.Heatmap(z=arg, zmin=0, zmax=1.0), row=a + 1, col=1)
#     fig.show()

'''
    df = pd.read_csv('data/NTM Ablation 1.0 Train.csv')
    fig = px.line(df, y='loss', color='name', title='Ablation 1.0 Loss')
    fig.show()

    df = pd.read_csv('data/NTM Ablation 1.0 Test.csv')
    df = df.groupby('name').mean()
    fig = px.bar(df, y='loss', title='Ablation 1.0 Test Loss')
    fig.show()
'''
