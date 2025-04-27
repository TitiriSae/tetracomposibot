# Clear l'écran
Clear-Host

# Mode d'affichage
$display_mode = 1

# Boucle de 0 à 4
for ($mapId = 0; $mapId -le 4; $mapId++) {
    Write-Host "Arena: $mapId"
    
    # Pour initPos True puis False
    foreach ($initPos in $true, $false) {
        python tetracomposibot.py config_Paintwars $mapId $initPos $display_mode
    }
}
