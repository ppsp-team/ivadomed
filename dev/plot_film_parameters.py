import sys
import os
import json
import matplotlib

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import seaborn as sns

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def plot_histogram(data, layer_no, fname_out):
    bins = np.linspace(-10, 10, 100)

    fig = plt.figure(figsize=(12, 12))
    plt.title(f'Histogram: Layer {layer_no}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.hist(data.ravel(), bins)
    fig.savefig(fname_out)


def visualize_pca(data, contrast_images, layer_no, fname_out):
    pca_df = pd.DataFrame()

    pca = PCA(n_components=3)

    for i in range(num_batch):
        pca_result = pca.fit_transform(data[i])
        pca_df2 = pd.DataFrame()
        pca_df2['pca1'] = pca_result[:, 0]
        pca_df2['pca2'] = pca_result[:, 1]
        pca_df2['pca3'] = pca_result[:, 2]
        pca_df2['contrast'] = contrast_images[i]
        pca_df = pd.concat([pca_df, pca_df2])

    # Create the graph and save it
    fig = plt.figure(figsize=(16,10))
    plt.title(f"PCA: Layer {layer_no}")
    sns.scatterplot(
        x="pca1", y="pca2",
        hue="contrast",
        data=pca_df,
        legend="full",
        alpha=1)
    fig.savefig(fname_out)


def visualize_tsne(data, contrast_images, layer_no, fname_out):
    tsne_df = pd.DataFrame()

    tsne = TSNE(n_components=2, verbose=1, perplexity=40, n_iter=300)

    for i in range(num_batch):
        tsne_results = tsne.fit_transform(data[i])
        tsne_df2 = pd.DataFrame()

        tsne_df2['tsne-2d-one'] = tsne_results[:, 0]
        tsne_df2['tsne-2d-two'] = tsne_results[:, 1]
        tsne_df2['contrast'] = contrast_images[i]

        tsne_df = pd.concat([tsne_df, tsne_df2])

    print('t-SNE done!')

    # Visualize
    fig = plt.figure(figsize=(16,10))
    plt.title(f"t-SNE: Layer {layer_no}")
    sns.scatterplot(
        x="tsne-2d-one",
        y="tsne-2d-two",
        hue="contrast",
        data=tsne_df,
        legend="full",
        alpha=1
    )
    plt.xlim(-260, 500)
    plt.ylim(-500, 500)
    fig.savefig(fname_out)

def run_main(context):

    log_dir = context["log_directory"]

    num_batch = 142

    gammas = {i: np.load(log_dir + f"/gammas_layer_{i}.npy") for i in range(1, 9)}
    betas = {i: np.load(log_dir + f"/betas_layer_{i}.npy") for i in range(1, 9)}
    contrast_images = np.load(log_dir + "contrast_images.npy")

    out_dir = log_dir + "/FiLM-parameters-visualization/"
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # save histograms with gammas and betas values
    for layer_no in range(1,9):
        plot_histogram(gammas[layer_no], layer_no, out_dir + f"hist_gammas_{layer_no}.png")
        plot_histogram(betas[layer_no], layer_no, out_dir + f"hist_betas_{layer_no}.png")

    # save PCA for betas and gammas except for the last layer due to gammas/betas shapes
    for layer_no in range(1,8):
        visualize_pca(gammas[layer_no], contrast_images, layer_no, out_dir + f"pca_gammas_{layer_no}.png")
        visualize_pca(betas[layer_no], contrast_images, layer_no, out_dir + f"pca_betas_{layer_no}.png")

    # save tsne for betas and gammas
    for layer_no in range(1,9):
        visualize_tsne(gammas[layer_no], contrast_images, layer_no, out_dir + f"tsne_gammas_{layer_no}.png")
        visualize_tsne(betas[layer_no], contrast_images, layer_no, out_dir + f"tsne_betas_{layer_no}.png")

if __name__ == "__main__":
    fname_config_file = sys.argv[1]

    with open(fname_config_file, "r") as fhandle:
        context = json.load(fhandle)

    run_main(context)