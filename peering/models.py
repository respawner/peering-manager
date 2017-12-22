from __future__ import unicode_literals

import ipaddress

from django.db import models
from django.urls import reverse
from django.utils import timezone

from .fields import ASNField, CommunityField
from .peeringdb import PeeringDB


class AutonomousSystem(models.Model):
    asn = ASNField()
    name = models.CharField(max_length=128)
    comment = models.TextField(blank=True)
    ipv6_as_set = models.CharField(max_length=128, blank=True, null=True)
    ipv4_as_set = models.CharField(max_length=128, blank=True, null=True)
    ipv6_max_prefixes = models.PositiveIntegerField(blank=True, null=True)
    ipv4_max_prefixes = models.PositiveIntegerField(blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['asn']

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(AutonomousSystem, self).save(*args, **kwargs)

    def get_peering_sessions_count(self):
        return self.peeringsession_set.count()

    def get_internet_exchanges(self):
        internet_exchanges = []

        for session in self.peeringsession_set.all():
            if session.internet_exchange not in internet_exchanges:
                internet_exchanges.append(session.internet_exchange)

        return internet_exchanges

    def get_internet_exchanges_count(self):
        return len(self.get_internet_exchanges())

    def get_absolute_url(self):
        return reverse('peering:as_details', kwargs={'asn': self.asn})

    def sync_with_peeringdb(self):
        peeringdb_info = PeeringDB().get_autonomous_system(self.asn)

        if not peeringdb_info:
            return False

        self.name = peeringdb_info.name
        self.ipv6_max_prefixes = peeringdb_info.info_prefixes6
        self.ipv4_max_prefixes = peeringdb_info.info_prefixes4
        self.save()

        return True

    def __str__(self):
        return 'AS{} - {}'.format(self.asn, self.name)


class Community(models.Model):
    name = models.CharField(max_length=128)
    value = CommunityField(max_length=50)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'communities'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('peering:community_details', kwargs={'id': self.id})

    def __str__(self):
        return self.name


class ConfigurationTemplate(models.Model):
    name = models.CharField(max_length=128)
    template = models.TextField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        self.updated = timezone.now()
        super(ConfigurationTemplate, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('peering:configuration_template_details', kwargs={'id': self.id})

    def __str__(self):
        return self.name


class InternetExchange(models.Model):
    peeringdb_id = models.PositiveIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    ipv6_address = models.GenericIPAddressField(blank=True, null=True)
    ipv4_address = models.GenericIPAddressField(blank=True, null=True)
    comment = models.TextField(blank=True)
    configuration_template = models.ForeignKey(
        'ConfigurationTemplate', blank=True, null=True, on_delete=models.SET_NULL)
    router = models.ForeignKey(
        'Router', blank=True, null=True, on_delete=models.SET_NULL)
    communities = models.ManyToManyField('Community', blank=True)

    class Meta:
        ordering = ['name']

    def get_peering_sessions_count(self):
        return self.peeringsession_set.count()

    def get_autonomous_systems(self):
        autonomous_systems = []

        for session in self.peeringsession_set.all():
            if session.autonomous_system not in autonomous_systems:
                autonomous_systems.append(session.autonomous_system)

        return autonomous_systems

    def get_autonomous_systems_count(self):
        return len(self.get_autonomous_systems())

    def get_absolute_url(self):
        return reverse('peering:ix_details', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name


class PeeringSession(models.Model):
    autonomous_system = models.ForeignKey(
        'AutonomousSystem', on_delete=models.CASCADE)
    internet_exchange = models.ForeignKey(
        'InternetExchange', on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    comment = models.TextField(blank=True)

    def to_dict(self):
        ip_version = ipaddress.ip_address(str(self.ip_address)).version

        # Enforce max prefixes to be set to 0 by default
        max_prefixes = 0

        # Set max prefixes based on IP version
        if ip_version == 6 and self.autonomous_system.ipv6_max_prefixes:
            max_prefixes = self.autonomous_system.ipv6_max_prefixes
        if ip_version == 4 and self.autonomous_system.ipv4_max_prefixes:
            max_prefixes = self.autonomous_system.ipv4_max_prefixes

        return {
            'peer_as': self.autonomous_system.asn,
            'peer_as_name': self.autonomous_system.name,
            'ip_version': ip_version,
            'ip_address': self.ip_address,
            'max_prefixes': max_prefixes,
        }

    def get_absolute_url(self):
        return reverse('peering:peering_session_details', kwargs={'id': self.id})

    def __str__(self):
        return '{} - AS{} - IP {}'.format(self.internet_exchange.name, self.autonomous_system.asn, self.ip_address)


class Router(models.Model):
    # Platform constants, based on NAPALM drivers
    PLATFORM_JUNOS = 'junos'
    PLATFORM_IOSXR = 'iosxr'
    PLATFORM_NONE = None
    PLATFORM_CHOICES = (
        (PLATFORM_JUNOS, 'Juniper JUNOS'),
        (PLATFORM_IOSXR, 'Cisco IOS-XR'),
        (PLATFORM_NONE, 'Other'),
    )

    name = models.CharField(max_length=128)
    hostname = models.CharField(max_length=256)
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, blank=True,
                                help_text='The router platform, used to interact with it')
    comment = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('peering:router_details', kwargs={'id': self.id})

    def __str__(self):
        return self.name
