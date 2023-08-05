---@class ZiplineAPI
local ZiplineAPI = {
    BaseURL = "http://yanille.home:8080",
    Announced = false,
    ---@type BindableEvent
    Emitter = Instance.new("BindableEvent", script),
    ---@type table | nil
    ApiDump = nil
}
local HttpService = game:GetService("HttpService")

function ZiplineAPI:Announce(name)
    if self.Announced then
        return true
    end

    self.Emitter:Fire("announcing")

    local response = HttpService:RequestAsync {
        Url = self.BaseURL .. "/announce",
        Method = "POST",
        Headers = {
            ["Content-Type"] = "application/json"
        },
        Body = HttpService:JSONEncode({ name = name })
    }

    self.Announced = response.Success
    if response.Success then
        self.SessionId = HttpService:JSONDecode(response.Body).sessionId

        print("Announced with SessionId: " .. self.SessionId)
    end

    self.Emitter:Fire("announced", self.Announced)

    return response.Success
end

function ZiplineAPI:Leave()
    if not self.Announced then
        return false
    end

    self.Emitter:Fire("leaving")

    local success, response = pcall(function()
        return HttpService:RequestAsync {
            Url = self.BaseURL .. "/announce",
            Method = "DELETE",
            Headers = {
                ["Content-Type"] = "text/plain",
                ["Authorization"] = "Bearer " .. self.SessionId
            },
            Body = ""
        }
    end)

    if not success then
        print("Failed to send leave, forcefully disconnecting...")

        self.Announced = false
        self.Emitter:Fire("left", true)

        return true
    end

    self.Announced = not response.Success
    if response.Success then
        print("ZiplineAPI left the building")
    end

    self.Emitter:Fire("left", response.Success)

    return response.Success
end

function ZiplineAPI:GetChangelist()
    local response = HttpService:RequestAsync {
        Url = self.BaseURL .. "/changelist",
        Method = "GET",
        Headers = {
            ["Content-Type"] = "text/plain",
            ["Authorization"] = "Bearer " .. self.SessionId
        }
    }

    return HttpService:JSONDecode(response.Body)
end

function ZiplineAPI:DeleteChanges(changes)
    local body = {
        changes = changes
    }

    local response = HttpService:RequestAsync {
        Url = self.BaseURL .. "/changelist",
        Method = "DELETE",
        Headers = {
            ["Content-Type"] = "application/json",
            ["Authorization"] = "Bearer " .. self.SessionId
        },
        Body = HttpService:JSONEncode(body)
    }

    return response.Success
end

function ZiplineAPI:CreatePackage(changes)
    local body = {
        changes = changes
    }

    local response = HttpService:RequestAsync {
        Url = self.BaseURL .. "/package",
        Method = "POST",
        Headers = {
            ["Content-Type"] = "application/json",
            ["Authorization"] = "Bearer " .. self.SessionId
        },
        Body = HttpService:JSONEncode(body)
    }

    if response.Success then
        return HttpService:JSONDecode(response.Body).id
    end

    return response.Success
end

function ZiplineAPI:DeletePackage(package)
    local body = {
        packageId = package
    }

    local response = HttpService:RequestAsync {
        Url = self.BaseURL .. "/package",
        Method = "DELETE",
        Headers = {
            ["Content-Type"] = "application/json",
            ["Authorization"] = "Bearer " .. self.SessionId
        },
        Body = HttpService:JSONEncode(body)
    }

    return response.Success
end

function ZiplineAPI:GetPackage(package)
    local response = HttpService:RequestAsync {
        Url = self.BaseURL .. "/package?id=" .. package,
        Method = "GET",
        Headers = {
            ["Authorization"] = "Bearer " .. self.SessionId
        }
    }

    if response.Success then
        return HttpService:JSONDecode(response.Body)
    end

    return response.Success
end

function ZiplineAPI:SaveInstance(instancePath, jsonInstanceString)
    local response = HttpService:RequestAsync {
        Url = self.BaseURL .. "/instance/" .. instancePath,
        Method = "POST",
        Headers = {
            ["Content-Type"] = "application/json",
            ["Authorization"] = "Bearer " .. self.SessionId
        },
        Body = jsonInstanceString
    }

    return response.Success
end

function ZiplineAPI:GetAPIDump()
    if self.ApiDump then
        return self.ApiDump
    end

    local response = HttpService:RequestAsync {
        Url = self.BaseURL .. "/roblox-api-dump",
        Method = "GET",
        Headers = {
            ["Authorization"] = "Bearer " .. self.SessionId
        }
    }

    if response.Success then
        self.ApiDump = HttpService:JSONDecode(response.Body)
        return self.ApiDump
    end

    return response.Success
end

return ZiplineAPI
