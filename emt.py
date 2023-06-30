'''
EMT federate 
'''

import helics as h
import random 

'''
Test docs
'''


def EMT():

    # HELICS federate initialization
    fedinitstring = "--federates=1 --brokerport=33000"

    # Create Federate Info object that describes the federate properties #
    fedinfo = h.helicsCreateFederateInfo()

    # Set Core name #
    # h.helicsFederateInfoSetCoreName(fedinfo, "EMT")

    # HELICS core type
    h.helicsFederateInfoSetCoreTypeFromString(fedinfo, "zmq")

    # Federate init string #
    h.helicsFederateInfoSetCoreInitString(fedinfo, fedinitstring)

    # Simulation resolution deltat
    deltat = 1.0
    h.helicsFederateInfoSetTimeProperty(fedinfo, h.helics_property_time_delta, deltat)

    # Value federate called EMT
    vfed = h.helicsCreateValueFederate("EMT", fedinfo)

    # Boundary buses between EMT and Phasor 
    N = [3,4,5,9]
    publications = {}
    subscriptions = {}
    vals = ["i_real", "i_imag", "v_real", "v_imag"]
    pub_vals = ["P","Q"]
    for ii in N: 
        for jj in vals:
            sub_name = f"Phasor_{ii}_{jj}"
            subscriptions[sub_name] = h.helicsFederateRegisterSubscription(vfed, sub_name, "")
        for kk in pub_vals: 
            pub_name = f"EMT_{ii}_{kk}"
            publications[pub_name] =  h.helicsFederateRegisterGlobalTypePublication(vfed, pub_name, "double", "")
    

    h.helicsFederateEnterExecutingMode(vfed)

    print("EMT entered execution mode")

    

    start_time = 0.0
    end_time = 10.0
    helicstime = start_time


    while abs(end_time - helicstime) > deltat:

        # Publish values to Phasor
        publication_sent = {}
        for key in publications.keys():
            pub = publications[key]
            value_to_send = random.random()
            h.helicsPublicationPublishDouble(pub, value_to_send)
            publication_sent[key] = value_to_send
        print(f"Time: {helicstime} ,EMT sent: {publication_sent}")

         # advance deltat timesteps

        helicstime = h.helicsFederateRequestTime(vfed, deltat)


        # Subscribe values from Phasor
        subscription_received = {}
        try:
            for key in subscriptions.keys():
                sub = subscriptions[key]
                value_recv = h.helicsInputGetDouble(sub)
                subscription_received[key] = value_recv
        except Exception as e: 
            print("No communciation at this time")
        print(f"Time: {helicstime} ,EMT received: {subscription_received}")

    h.helicsFederateDisconnect(vfed)
    h.helicsFederateFree(vfed)

    return 



if __name__ == "__main__":
    EMT()