import torch
import pandas as pd
import numpy as np

class H5Dataset(torch.utils.data.Dataset):
    
    def __init__(self, samples, target_name, size = None, feature_names = None, 
                 scale = False, labels = None):
        super(H5Dataset, self).__init__()

        # Load all samples, adding a sample number
        dfs = []
        for i,path in enumerate(samples):            
            dfs.append(pd.read_hdf(path))
            dfs[i]["sample"] = i
            
            if labels and len(labels) == len(samples):
                dfs[i]["label"] = labels[i]
            
            if size is not None:
                dfs[i] = dfs[i][:size]
            
            print(f"Loading {len(dfs[i])} entries {path}")
            
        self.df = pd.concat(dfs)
        
        # Find target
        self.target = self.df.pop(target_name).values.reshape(-1, 1)

        # Find features and labels
        if feature_names:
            self.feature_names = feature_names
        else:
            self.feature_names = [c for c in self.df.columns.values 
                                  if not "mmc" in c.lower() and not "svfit" in c.lower()
                                  and not c == "sample"]

        self.features = self.df[self.feature_names].values

        # Auxilary (non-training) vars
        self.extra_names = list(set(self.df.columns.values) - set(self.feature_names))
        self.extra = self.df[self.extra_names].values
                 
        if scale:
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            scaler.fit(self.features)
            self.features = scaler.transform(self.features)
        
    def X(self):
        return self.features
    
    def y(self):
        return self.target
    
    def labels(self):
        return self.feature_names
    
    def aux_labels(self):
        return self.extra_names
    
    def aux(self, name = ""):
        if not name:
            return self.extra
        
        try:
            idx = self.extra_names.index(name)
            return self.extra[:, idx]
            
        except ValueError:
            return None
    
        
    def __getitem__(self, index):        
        return (torch.tensor(self.features[index], dtype=torch.float32),
                torch.tensor(self.target[index], dtype=torch.float32))

    def __len__(self):
        return self.features.shape[0]