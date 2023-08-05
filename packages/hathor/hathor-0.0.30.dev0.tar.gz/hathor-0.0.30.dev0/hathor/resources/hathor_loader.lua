local HATHOR_ROOT = script.Parent
local HATHOR_CACHE = {}

local RunService = game:GetService("RunService")
local deleteModules = not RunService:IsStudio()

local function __require(require_str)
    if HATHOR_CACHE[require_str] then
        return HATHOR_CACHE[require_str]
    end

    local instance = HATHOR_ROOT:WaitForChild(require_str, 3)
    assert(instance, "Did not find a module in time")

    local loaded = require(instance)
    HATHOR_CACHE[require_str] = loaded

    if type(loaded) == "table" and loaded.Init and type(loaded.Init) == "function" then
        loaded:Init()
    end

    if deleteModules then
        instance.Name = instance.ClassName
        instance:Destroy()
    end

    return loaded
end

return __require
