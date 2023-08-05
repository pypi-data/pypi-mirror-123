---@type ZiplineAPI
local ZiplineAPI = require(script.Parent.ZiplineAPI)

---@type HttpService
local HttpService = game:GetService("HttpService")

local API_DUMP_BY_CLASS_NAME

local function getApiDump()
    return ZiplineAPI:GetAPIDump()
end

local function getApiDumpByClassName()
    if API_DUMP_BY_CLASS_NAME then
        return API_DUMP_BY_CLASS_NAME
    end

    API_DUMP_BY_CLASS_NAME = {}

    for _, classSpecification in pairs(getApiDump()["Classes"]) do
        API_DUMP_BY_CLASS_NAME[classSpecification["Name"]] = classSpecification
    end

    return API_DUMP_BY_CLASS_NAME
end

local function isValidClassName(className)
    for apiDumpClassName, _ in pairs(getApiDumpByClassName()) do
        if apiDumpClassName == className then
            return true
        end
    end

    return false
end

local VALUE_SERIALIZERS = {
    ---@param v Vector3
    Vector3 = function(s, v)
        return { v.X, v.Y, v.Z }
    end,
    ---@param v Vector2
    Vector2 = function(s, v)
        return { v.X, v.Y }
    end,
    ---@param v Color3
    Color3 = function(s, v)
        return { v.R, v.G, v.B }
    end,
    ---@param v UDim2
    UDim2 = function(s, v)
        return {
            v.X.Scale, v.X.Offset,
            v.Y.Scale, v.Y.Offset
        }
    end,
    ---@param v UDim
    UDim = function(s, v)
        return { v.Scale, v.Offset }
    end,
    ---@param v TweenInfo
    TweenInfo = function(s, v)
        return {
            v.Time,
            v.EasingStyle.Name,
            v.EasingDirection.Name,
            v.RepeatCount,
            v.Reverses,
            v.DelayTime
        }
    end,
    ---@param v Region3
    Region3 = function(s, v)
        return {
            v.CFrame:GetComponents(),
            v.Size.X,
            v.Size.Y,
            v.Size.Z,
        }
    end,
    ---@param v Rect
    Rect = function(s, v)
        return {
            v.Min.X,
            v.Min.Y,
            v.Max.X,
            v.Max.Y
        }
    end,
    ---@param v RaycastResult
    RaycastResult = function(s, v)
        return {
            s.idLookupTable[v.Instance],
            v.Position.X,
            v.Position.Y,
            v.Position.Z,
            v.Material.Name,
            v.Normal.X,
            v.Normal.Y,
            v.Normal.Z
        }
    end,
    ---@param v Ray
    Ray = function(s, v)
        return {
            v.Origin.X,
            v.Origin.Y,
            v.Origin.Z,
            v.Direction.X,
            v.Direction.Y,
            v.Direction.Z
        }
    end,
    ---@param v PhysicalProperties
    PhysicalProperties = function(s, v)
        return {
            v.Density,
            v.Friction,
            v.Elasticity,
            v.FrictionWeight,
            v.ElasticityWeight
        }
    end,
    ---@param v PathWaypoint
    PathWaypoint = function(s, v)
        return {
            v.Position.X,
            v.Position.Y,
            v.Position.Z,
            v.Action.Name
        }
    end,
    ---@param v NumberSequenceKeypoint
    NumberSequenceKeypoint = function(s, v)
        return {
            v.Time,
            v.Value,
            v.Envelope
        }
    end,
    ---@param v NumberSequence
    NumberSequence = function(s, v)
        local serializedValue = {}

        for _, keypoint in pairs(v.Keypoints) do
            table.insert(serializedValue, {
                keypoint.Time,
                keypoint.Value,
                keypoint.Envelope
            })
        end

        return serializedValue
    end,
    ---@param v NumberRange
    NumberRange = function(s, v)
        return {
            v.Min,
            v.Max
        }
    end,
    ---@param v Instance
    Instance = function(s, v)
        return { s.idLookupTable[v] }
    end,
    ---@param v Faces
    Faces = function(s, v)
        return {
            v.Top,
            v.Bottom,
            v.Left,
            v.Right,
            v.Back,
            v.Front
        }
    end,
    ---@param v DateTime
    DateTime = function(s, v)
        return { v:ToIsoDate() }
    end,
    ---@param v ColorSequenceKeypoint
    ColorSequenceKeypoint = function(s, v)
        return {
            v.Time,
            {
                v.Value.R,
                v.Value.G,
                v.Value.B,
            }
        }
    end,
    ---@param
    ColorSequence = function(s, v)
        local serializedValue = {}

        for _, keypoint in pairs(v.Keypoints) do
            table.insert(serializedValue, {
                keypoint.Time,
                {
                    keypoint.Value.R,
                    keypoint.Value.G,
                    keypoint.Value.B
                }
            })
        end

        return serializedValue
    end,
    ---@param v CFrame
    CFrame = function(s, v)
        return { v:GetComponents() }
    end,
    ---@param v BrickColor
    BrickColor = function(s, v)
        return {
            v.Name,
            v.Number,
            v.Color.R,
            v.Color.G,
            v.Color.B
        }
    end,
    ---@param v Axes
    Axes = function(s, v)
        return {
            v.X,
            v.Y,
            v.Z,
            v.Top,
            v.Bottom,
            v.Left,
            v.Right,
            v.Back,
            v.Front
        }
    end,
    ---@param v LocalizationTable
    LocalizationTable = function(s, v)
        return {
            v.SourceLocaleId,
            v:GetEntries()
        }
    end
}

VALUE_SERIALIZERS["Vector3int16"] = VALUE_SERIALIZERS["Vector3"]
VALUE_SERIALIZERS["Vector2int16"] = VALUE_SERIALIZERS["Vector2"]
VALUE_SERIALIZERS["Region3int16"] = VALUE_SERIALIZERS["Region3"]

---@param rootInstance Instance
---@return table<Instance>
local function generateInstanceList(rootInstance)
    local instanceList = { rootInstance }

    for _, descendant in pairs(rootInstance:GetDescendants()) do
        table.insert(instanceList, descendant)
    end

    return instanceList
end

---@param instanceList table<Instance>
---@return table<Instance, string>
local function generateLookupTable(instanceList)
    local idLookupTable = {}

    for _, instance in pairs(instanceList) do
        idLookupTable[instance] = HttpService:GenerateGUID(false)
    end

    return idLookupTable
end

local function containsTag(classMember, tag)
    local tags = classMember["Tags"]

    if tags then
        for _, classTag in pairs(tags) do
            if classTag:lower() == tag:lower() then
                return true
            end
        end
    end

    return false
end

local function canSerialize(classMember)
    local disqualifiedTags = {
        "Deprecated",
        "NotScriptable",
        "ReadOnly"
    }

    for _, tag in pairs(disqualifiedTags) do
        if containsTag(classMember, tag) then
            return false
        end
    end

    local security = classMember["Security"]

    if security then
        local readSecurity = security["Read"]
        local writeSecurity = security["Write"]

        if readSecurity and readSecurity == "None" and writeSecurity and writeSecurity == "None" then
            return true
        end
    end

    return false
end

local function processAttributes(instance, processedInstance)
    local attributes = instance:GetAttributes()

    local attributeCount = 0
    for _, __ in pairs(attributes) do
        attributeCount = attributeCount + 1
    end

    if attributeCount <= 0 then
        return processedInstance
    end

    local processedAttributes = {}
    for k, v in pairs(attributes) do
        local valueType = typeof(v)
        local serializer = VALUE_SERIALIZERS[valueType]

        local success, serializedValue = pcall(function()
            if serializer then
                return serializer({}, v)
            end

            return nil
        end)

        if not (success and serializedValue) then
            if type(v) == "userdata" then
                serializedValue = tostring(v)

            else
                serializedValue = v
            end
        end

        processedAttributes[k] = {
            Type = valueType,
            Value = serializedValue
        }
    end

    processedInstance.Attributes = processedAttributes

    return processedInstance
end

local function processMembers(session, instance, processedInstance, className)
    local classSpecification = getApiDumpByClassName()[className or instance.ClassName]

    for _, classMember in pairs(classSpecification["Members"]) do
        if classMember["MemberType"] == "Property" and canSerialize(classMember) then
            local propertyName = classMember["Name"]
            local value = instance[propertyName]
            local valueTypeCategory = classMember["ValueType"]["Category"]
            local valueTypeName = classMember["ValueType"]["Name"]
            local serializer = VALUE_SERIALIZERS[valueTypeName]
            local serializedValue = nil

            if valueTypeCategory == "Class" and isValidClassName(valueTypeName) then
                serializer = VALUE_SERIALIZERS.Instance
            end

            if serializer then
                -- print("Serializing property", propertyName, "on", instance:GetFullName())

                local success = pcall(function()
                    serializedValue = serializer(session, value)
                end)

                if not success then
                    print("Failed serializing property", propertyName, "on", instance:GetFullName())
                end
            end

            if serializedValue == nil then
                if type(value) == "userdata" then
                    serializedValue = { tostring(value) }

                else
                    serializedValue = { value }

                end
            end

            processedInstance["Properties"][propertyName] = serializedValue
        end
    end

    local superClass = classSpecification["Superclass"]
    if superClass and superClass ~= "<<<ROOT>>>" then
        processedInstance = processMembers(session, instance, processedInstance, superClass)
    end

    return processedInstance
end

---@param rootInstance Instance
---@return string
local function serializeInstance(rootInstance)
    local instanceList = generateInstanceList(rootInstance)
    local idLookupTable = generateLookupTable(instanceList)
    local processedInstanceList = {}

    local session = {
        idLookupTable = idLookupTable
    }

    for _, instance in pairs(instanceList) do
        local processedInstance = processMembers(session, instance, {
            Id = idLookupTable[instance],
            ClassName = instance.ClassName,
            Properties = {

            }
        })

        processedInstance = processAttributes(instance, processedInstance)

        table.insert(processedInstanceList, processedInstance)
    end

    return HttpService:JSONEncode(processedInstanceList)
end

return serializeInstance
