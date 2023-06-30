'''
Phasor federate 
'''

import helics as h
import random 

'''
Test docs
'''


def Phasor():

    # HELICS federate initialization
    fedinitstring = "--federates=1 --brokerport=33000"

    # Create Federate Info object that describes the federate properties #
    fedinfo = h.helicsCreateFederateInfo()

    # Set Core name #
    # h.helicsFederateInfoSetCoreName(fedinfo, "Phasor")

    # HELICS core type
    h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")

    # Federate init string #
    h.helicsFederateInfoSetCoreInitString(fedinfo, fedinitstring)

    # Simulation resolution deltat
    deltat = 1.0
    h.helicsFederateInfoSetTimeProperty(fedinfo, h.helics_property_time_delta, deltat)

    # Value federate called Phasor
    vfed = h.helicsCreateValueFederate("Phasor", fedinfo)

    # Boundary buses between EMT and Phasor 
    N = [3,4,5,9]
    publications = {}
    subscriptions = {}
    vals = ["i_real", "i_imag", "v_real", "v_imag"]
    sub_vals = ["P","Q"]
    for ii in N: 
        for jj in vals:
            pub_name = f"Phasor_{ii}_{jj}"
            publications[pub_name] =  h.helicsFederateRegisterGlobalTypePublication(vfed, pub_name, "double", "")
        for kk in sub_vals: 
            sub_name = f"EMT_{ii}_{kk}"
            subscriptions[sub_name] = h.helicsFederateRegisterSubscription(vfed, sub_name, "")
    

    h.helicsFederateEnterExecutingMode(vfed)

    print("Phasor entered execution mode")

    

    start_time = 0.0
    end_time = 10.0
    helicstime = start_time


    while abs(end_time - helicstime) > deltat:

        # advance deltat timesteps
        helicstime = h.helicsFederateRequestTime(vfed, deltat)

        # Subscribe values from EMT
        subscription_received = {}
        try:
            for key in subscriptions.keys():
                sub = subscriptions[key]
                value_recv = h.helicsInputGetDouble(sub)
                subscription_received[key] = value_recv
        except Exception as e: 
            print("No communciation at this time")
        print(f"Time: {helicstime} ,Phasor received: {subscription_received}")


        # Publish values to EMT
        publication_sent = {}
        for key in publications.keys():
            pub = publications[key]
            value_to_send = random.random()
            h.helicsPublicationPublishDouble(pub, value_to_send)
            publication_sent[key] = value_to_send
        print(f"Time: {helicstime} ,Phasor sent: {publication_sent}")

    h.helicsFederateDisconnect(vfed)
    h.helicsFederateFree(vfed)

    return 



if __name__ == "__main__":
    Phasor()