import click
import networkx as nx
import modelos

@click.group()
def cli():
    """
    Simple CLI for producing network models
    """


@cli.command()
@click.option('--n', default=500, help='number of nodes')
@click.option('--m', default=3, help='indicates the m value, must be m < n')

def barabasi_albert(n,m):
    click.echo('generating barabasi albert model with n = {}, m = {}'.format(n,m))
    ba = modelos.barabasi_albert(n,m)
    nx.write_edgelist(ba, "barabasi_albert_n{}_m{}.csv".format(n, m), delimiter=",", data=True)

@cli.command()
@click.option('--n', default=500, help='number of nodes')
@click.option('--p', default=0.01, help='indicates the p value, probability')
@click.option('--total', default=1, help='indicate how many random graphs do you want')

def erdos_renyi(n,p,total):
    click.echo('generating {} erdos renyi model(s) with n = {}, p = {}'.format(total,n,p))
    for i in range(total):
        er = modelos.random_graph(n,p)
        nx.write_edgelist(er, 'erdos_renyi_{}_n{}_p{}.csv'.format(i,n,p), delimiter=",", data=True)

if __name__ == "__main__":
    cli()