import pandas as pd

class autoOverlay:
    def __init__(self, strings, bases):
        self.df = pd.DataFrame()
        self.strings = strings
        self.bases = bases
        
        self.iterate_bases()
        
    def iterate_bases(self):
        for base in self.bases:
            print(base)
            dd = pd.DataFrame()
            for key, value in self.strings.items():
                dd[key] = self.get_attributes(base, key, value)
            self.df = self.df.append(dd)
            
        for col in self.df:
            self.df[col] = self.df[col].astype(str).str.replace("[","").str.replace("]","")
            self.df[col] = self.df[col].astype(str).str.replace("'","")
        
    def get_attributes(self, lyrname, overlayname, spnr):
        df = pd.DataFrame()
        
        layer = QgsProject.instance().mapLayersByName(lyrname)[0]
        overlay = QgsProject.instance().mapLayersByName(overlayname)[0]
        
        
        l = []
        for selectid in range(len([i for i in layer.getFeatures()])):
            layer.select(selectid)
            result = processing.run('native:clip', { 'INPUT' : overlay.source(),
                'OUTPUT' : 'TEMPORARY_OUTPUT',
                'OVERLAY' : QgsProcessingFeatureSourceDefinition(layer.source(), True) })

            x = []
            for num in spnr:
                x.append([i.attributes()[num] for i in result['OUTPUT'].getFeatures()])
            l.append(x)
            
            layer.removeSelection()
        
        return pd.Series(l)
        #self.df = self.df.append(df)
        
        
strings = {'geologische Formation': [4],
'Bodenhauptgruppen_50000': [6],
'Grundwasserkörper': [0,1], 
'FFH': [0,1],
'Vogelschutzgebiet': [0,0],
'Wasserschutzgebiet': [0,1],
'Naturschutzgebiet': [0,1],
'Landschaftsschutzgebiet': [0, 1],
'WRRL-Gewässer': [1],
'Überschwemmungsgebiet': [6],
'Hessische Biotopkartierung-Biotope': [4],
'Hessische Biotopkartierung-Biotope': [3],
'Npot_GW_MKK_2011_03_02': [17],
'Erosionsgefährdung nach WRRL': [1]
}
    
bases = ['BG_verknuepft',
    'BO_verknuepft',
    'BSS_verknuepft',
    'GN_verknuepft',]
    #    'WB_verknuepft'
    #     'SC_verknuepft',
    #     'ST_verknuepft',

x = autoOverlay(strings, bases)
print(x.df)
x.df.to_csv('csv.csv', sep='|',index=False,index_label=None)
