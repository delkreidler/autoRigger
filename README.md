# autoRigger for Maya
  A work in progress autoRigger for Maya. Currently can generate joints, chains, and simple fk chain.

# Installing
  Unzip the package and save inside your maya scripts folder. Then in maya run this code through the script editor to open the gui window:

  ```python
  import importlib
  from autoRigger import autoRigger
  importlib.reload(autoRigger)
  autoRigger.open_window()
  ```
  
