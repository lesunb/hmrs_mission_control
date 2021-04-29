import copy
from random import Random
from functools import partial

from deeco.core import Node
from deeco.packets import Packet
from deeco.runnable import SimPlugin
from deeco.runnable import NodePlugin


class SimpleNetworkDevice(NodePlugin):
	def __init__(self, node, network):
		super().__init__(node)

		self.network = network
		self.receivers = []

		# Provide access to this plugin
		node.networkDevice = self

	def add_receiver(self, receiver):
		self.receivers.append(receiver)

	def receive(self, packet, time_ms):
		for receiver in self.receivers:
			receiver(packet)

	def send(self, destination, packet: Packet):
		"""Send packet to destination, distance limit is not take into account"""
		self.network.send(destination, packet)

	def broadcast(self, packet: Packet):
		"""Broadcast packet within device range"""
		self.network.broadcast(packet, self)


class SimpleNetwork(SimPlugin):
	def __init__(self, sim, range_m=250, delay_ms_mu=0, delay_ms_sigma=0):
		super().__init__(sim)

		self.devices = {}

		self.random = Random()
		self.random.seed(42)

		self.range_m = range_m
		self.delay_ms_mu = delay_ms_mu
		self.delay_ms_sigma = delay_ms_sigma

	def attach_to(self, node: Node):
		super().attach_to(node)
		self.devices[node.id] = SimpleNetworkDevice(node, self)

	def deliver(self, device, packet: Packet):
		delivery = partial(device.receive, packet)
		self.sim.scheduler.set_timer(delivery, time_ms=self.__get_delivery_time_ms())

	def send(self, destination, packet: Packet):
		self.deliver(self.devices[destination], packet)

	def broadcast(self, packet: Packet, source: SimpleNetworkDevice):
		for address, device in self.devices.items():
			src_pos = source.node.positionProvider.get()
			dst_pos = device.node.positionProvider.get()
			if src_pos.dist_to(dst_pos) < self.range_m and device is not source:
				self.deliver(device, packet)

	def __get_delivery_time_ms(self):
		return self.sim.scheduler.get_time_ms() + self.random.normalvariate(self.delay_ms_mu, self.delay_ms_sigma)