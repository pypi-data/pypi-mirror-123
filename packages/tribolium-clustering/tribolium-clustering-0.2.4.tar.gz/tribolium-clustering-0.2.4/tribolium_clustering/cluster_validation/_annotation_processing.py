import pandas as pd
from pyclesperanto_prototype import statistics_of_background_and_labelled_pixels
from skimage.io import imread

def only_annotated_cells_combined_dataframe(dataset,timepoint,
                                            cluster_result_folder, cluster_result_file_name_prefix,
                                            annotation_folder,annotation_file_name_prefix,annotation_column_name,
                                           ):
    
    
    cluster_prediction_csv = pd.read_csv(cluster_result_folder+
                                                   cluster_result_file_name_prefix+ 
                                                   't{}.csv'.format(timepoint))
    try:
        cluster_prediction_csv = cluster_prediction_csv.drop(['Unnamed: 0'], axis=1)
    except KeyError:
        print('No Unnamed Column!')
    
    labels = dataset.get_labels(timepoint)
    annotation_img = imread(annotation_folder+ 
                              annotation_file_name_prefix + 
                              't{}.tif'.format(timepoint))
    

    cle_regionp = statistics_of_background_and_labelled_pixels(annotation_img,labels)
    annotated_labels = cle_regionp['max_intensity'][1:].astype('uint8')
    
    annotation_df = pd.DataFrame({annotation_column_name:annotated_labels})
    cluster_pred_and_annotation = pd.concat([cluster_prediction_csv,annotation_df], axis = 1)
    
    only_annotated_subset = cluster_pred_and_annotation[cluster_pred_and_annotation[annotation_column_name]>0]
    return only_annotated_subset