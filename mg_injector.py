import services
import sims4.resources
import mg_logger

# =========================================================================
# Deine generierten IDs aus dem Sims 4 Studio
# =========================================================================
UI_INTERACTION_IDS = [
    11740034960776599168, # Option 1
    11740034960776599171, # Option 2
    11740034960776599170, # Option 3
    5042506799666156107   # Household
]

def inject_to_sims(*args, **kwargs):
    if not UI_INTERACTION_IDS:
        return
        
    instance_manager = services.get_instance_manager(sims4.resources.Types.INTERACTION)
    if not instance_manager:
        return

    # 14798 = sim-sim (Klick auf andere) | 14714 = sim-picker (Klick auf sich selbst)
    target_tunings = [14798, 14714]
    injected_count = 0
    
    for tuning_id in target_tunings:
        sim_tuning = instance_manager.get(tuning_id)
        if not sim_tuning:
            continue

        affordances = getattr(sim_tuning, '_super_affordances', None)
        if affordances is None:
            continue

        affordances_tuple = list(affordances)
        added = False
        
        for int_id in UI_INTERACTION_IDS:
            int_instance = instance_manager.get(int_id)
            if int_instance and int_instance not in affordances_tuple:
                affordances_tuple.append(int_instance)
                added = True

        if added:
            setattr(sim_tuning, '_super_affordances', tuple(affordances_tuple))
            injected_count += 1

    if injected_count > 0:
        mg_logger.log(f"[UI] Menue-Optionen erfolgreich in {injected_count} Sim-Zustaende injiziert.")

try:
    from sims4.callbacks import add_callback, CallbackType
    add_callback(CallbackType.ON_TUNING_LOADED, inject_to_sims)
    
    if services.get_instance_manager(sims4.resources.Types.INTERACTION).all_instances_loaded:
        inject_to_sims()
except:
    pass