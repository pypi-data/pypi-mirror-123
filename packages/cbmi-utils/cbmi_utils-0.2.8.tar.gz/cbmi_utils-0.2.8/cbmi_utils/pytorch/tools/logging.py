import logging

def print_learnable_params(model, freezed_too=True):
    """ Print (learnable) parameters in a given network model

    Args:
        model: Model you want to print the learned parameters
        freezed_too: Print the freezed parameters as well
    """
    logger = logging.getLogger()
    updated = []
    freezed = []

    for name, param in model.named_parameters():
        if param.requires_grad:
            updated.append(name)
        else:
            freezed.append(name)

    logger.info("-- Following parameters will be updated:")

    for para in updated:
        logger.info(f"  -- {para}")
    if freezed_too is True:
        logger.info("-- Following parameters are freezed:")
        for para in freezed:
            logger.info(f"  -- {para}")