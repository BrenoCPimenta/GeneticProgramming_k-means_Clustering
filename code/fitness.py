from sklearn.metrics.cluster import v_measure_score
from pyclustering.cluster.kmeans import kmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils.metric import distance_metric, type_metric

from subject import SubjectTree


def FitnessCLustering(seed, k, X, Y, euclidean=True, subject=None):
    # Inicializa centróides utilizando método K-Means++
    initial_centers = kmeans_plusplus_initializer(X, k, random_state=seed).initialize()

    if euclidean:# cria instância do K-Means utilizando distância Euclidiana
        kmeans_instance = kmeans(X, initial_centers, random_state=seed)
    else:
        subject_function = createFunctionFromSubject(subject)
        subject_metric = distance_metric(type_metric.USER_DEFINED, func=subject_function, random_state=seed)
        kmeans_instance = kmeans(X, initial_centers, metric=subject_metric, random_state=seed)
    # run cluster analysis and obtain results
    kmeans_instance.process()
    # recupera os clusters gerados
    clusters = kmeans_instance.get_clusters()

    #print("---> Gerou ", len(clusters), " clusters")
    for i in range(len(clusters)):
        # Setting label
        X.loc[clusters[i],'y_pred'] = i

    # FMI
    return v_measure_score(Y, X.y_pred)



def createFunctionFromSubject(subject_tree):
    def subject_funtion(point1, point2):
        variable_values = interlaceLists(point1, point2)
        return subject_tree.evalFunction(variable_values) 
    return subject_funtion

def interlaceLists(list1, list2):
    result = [None]*(len(list1)+len(list2))
    result[::2] = list1
    result[1::2] = list2
    return result