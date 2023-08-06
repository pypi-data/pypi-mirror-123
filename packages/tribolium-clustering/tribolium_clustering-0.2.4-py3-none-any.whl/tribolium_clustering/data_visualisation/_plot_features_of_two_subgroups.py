def plot_features_of_two_subgroups(regprops, subgroup1_mask, subgroup2_mask, feature_keys):
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns
    
    n_features_div2 = int(np.round(len(feature_keys)/2+0.1))
    
    fig, axs = plt.subplots(n_features_div2, 2, figsize = (15,30))


    for i,key in enumerate(feature_keys):
        prop = regprops[key]

        select1 = prop[subgroup1_mask].tolist()
        select2 = prop[subgroup2_mask].tolist()
        
        if i < n_features_div2:
            j = 0
            n = i
        else:
            j = 1
            n = i-n_features_div2
        
        kwargs = dict({'linewidth' : 0, 'alpha': 0.3})
        
        sns.histplot(select1, ax= axs[n,j], kde=True,color=sns.color_palette()[0], bins=20, **kwargs)
        sns.histplot(select2, ax= axs[n,j], kde=True,color=sns.color_palette()[1], bins=20, **kwargs)
        axs[n,j].set_title(key)