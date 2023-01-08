from enum import Enum


class SupportedCity(str, Enum):
    '''
    This enum defines the list of cities that the service currently
    will provides listing data for
    '''
    
    boston = 'Boston, MA'
    newYork = 'New York City, NY'
    seattle = 'Seattle, WA'
    # losAngeles = 'Los Angeles, CA'
    sanFran = 'San Francisco, CA'
    # sanJose = 'San Jose, CA'
    # philadelphia = 'Philadelphia, PA'
    # dc = 'Washington DC'
    # portland = 'Portland, OR'
    # chicago = 'Chicago, IL'
    # houston = 'Houston, TX'
    # phoenix = 'Phoenix, AZ'
    # sanAntonio = 'San Antonio, CA'
    # sanDiego = 'San Diego, CA'
    # dallas = 'Dallas, TX'
    # austin = 'Austin TX'
    # jacksonville = 'Jacksonville, FL'
    # fortWorth = 'Fort Worth, TX'
    # columbus = 'Columbus, OH'
    # charlotte = 'Charlotte, NC'
    # indianapolis = 'Indianapolis, IN'
    # denver = 'Denver, CO'