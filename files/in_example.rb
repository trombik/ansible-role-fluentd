require "fluent/input"

module Fluent
  # An example fluentd plug-in
  class Example < Input
    Fluent::Plugin.register_input("example", self)

    def configure(conf)
      super
    end

    def start
      super
    end

    def shutdown
      super
    end
  end
end
